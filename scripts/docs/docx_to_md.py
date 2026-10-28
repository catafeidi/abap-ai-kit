#!/usr/bin/env python3
"""Convert a Word specification (.docx) to Markdown for an AI assistant to read.

Specifications are reviewed in Word: deleted content is often only struck through, and reviewers
add requirements as comments. This converter therefore
  - drops tracked deletions (w:del) and struck-through text (w:strike / w:dstrike),
  - keeps Word comments, as a quote below the paragraph they belong to (author: text),
  - keeps headings, numbered and bulleted lists, tables, bold / italic / monospace,
  - marks images as [image: <name>] (the files stay in the .docx: word/media/).

Standard library only.

Usage:
  python docx_to_md.py <spec.docx> [<out.md>] [--keep-strike]
  without <out.md> the Markdown goes next to the .docx (<name>.md).
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W}


def q(tag):
    return f"{{{W}}}{tag}"


def read_xml(archive, name):
    try:
        return ET.fromstring(archive.read(name))
    except KeyError:
        return None


def style_names(styles):
    names = {}
    if styles is None:
        return names
    for style in styles.iter(q("style")):
        name = style.find("w:name", NS)
        names[style.get(q("styleId"))] = name.get(q("val")) if name is not None else ""
    return names


def numbering_formats(numbering):
    """numId -> {ilvl: numFmt}"""
    if numbering is None:
        return {}
    abstract = {}
    for item in numbering.iter(q("abstractNum")):
        levels = {}
        for lvl in item.iter(q("lvl")):
            fmt = lvl.find("w:numFmt", NS)
            levels[lvl.get(q("ilvl"))] = fmt.get(q("val")) if fmt is not None else "bullet"
        abstract[item.get(q("abstractNumId"))] = levels
    result = {}
    for num in numbering.iter(q("num")):
        ref = num.find("w:abstractNumId", NS)
        if ref is not None:
            result[num.get(q("numId"))] = abstract.get(ref.get(q("val")), {})
    return result


def comments_by_id(comments):
    found = {}
    if comments is None:
        return found
    for comment in comments.iter(q("comment")):
        text = " ".join(
            "".join(t.text or "" for t in p.iter(q("t"))).strip() for p in comment.iter(q("p"))
        ).strip()
        found[comment.get(q("id"))] = (comment.get(q("author")) or "?", text)
    return found


def flag(rpr, tag):
    if rpr is None:
        return False
    element = rpr.find(f"w:{tag}", NS)
    return element is not None and element.get(q("val")) not in ("0", "false", "none")


def escape(text):
    return re.sub(r"([|*`])", r"\\\1", text)


class Converter:
    def __init__(self, archive, keep_strike):
        self.keep_strike = keep_strike
        self.styles = style_names(read_xml(archive, "word/styles.xml"))
        self.numbering = numbering_formats(read_xml(archive, "word/numbering.xml"))
        self.comments = comments_by_id(read_xml(archive, "word/comments.xml"))
        self.used_comments = set()
        self.dropped_strike = 0
        rels = read_xml(archive, "word/_rels/document.xml.rels")
        self.images = {}
        if rels is not None:
            for rel in rels:
                self.images[rel.get("Id")] = Path(rel.get("Target", "")).name

    def runs(self, paragraph):
        parts, refs = [], []
        for node in paragraph.iter():
            if node.tag == q("commentReference"):
                refs.append(node.get(q("id")))
        for run in self._runs(paragraph):
            rpr = run.find("w:rPr", NS)
            text = ""
            for child in run:
                if child.tag == q("t"):
                    text += child.text or ""
                elif child.tag == q("tab"):
                    text += " "
                elif child.tag in (q("br"), q("cr")):
                    text += " "
                elif child.tag == q("drawing"):
                    blip = next((b for b in child.iter() if b.tag.endswith("}blip")), None)
                    rid = blip.get(f"{{{R}}}embed") if blip is not None else None
                    parts.append(f"[image: {self.images.get(rid, 'embedded')}]")
            if not text:
                continue
            if (flag(rpr, "strike") or flag(rpr, "dstrike")) and not self.keep_strike:
                self.dropped_strike += 1
                continue
            stripped = text.strip()
            if not stripped:
                parts.append(text)
                continue
            lead = text[: len(text) - len(text.lstrip())]
            trail = text[len(text.rstrip()):]
            fonts = rpr.find("w:rFonts", NS) if rpr is not None else None
            font = " ".join(fonts.attrib.values()) if fonts is not None else ""
            if re.search(r"Consolas|Courier|Mono", font, re.I):
                body = f"`{stripped}`"
            else:
                body = escape(stripped)
                if flag(rpr, "b"):
                    body = f"**{body}**"
                if flag(rpr, "i"):
                    body = f"*{body}*"
            parts.append(lead + body + trail)
        text = re.sub(r"\*\*\s*\*\*", "", "".join(parts))
        return re.sub(r"[ \t]+", " ", text).strip(), refs

    def _runs(self, element):
        for child in element:
            if child.tag == q("del"):
                continue
            if child.tag == q("r"):
                yield child
            elif child.tag in (q("ins"), q("hyperlink"), q("smartTag"), q("sdt"), q("sdtContent"),
                               q("fldSimple")):
                yield from self._runs(child)

    def comment_lines(self, refs):
        lines = []
        for ref in refs:
            if ref in self.comments and ref not in self.used_comments:
                self.used_comments.add(ref)
                author, text = self.comments[ref]
                lines.append(f"> **Comment ({author}):** {text}")
        return lines

    def paragraph(self, paragraph, counters):
        text, refs = self.runs(paragraph)
        notes = self.comment_lines(refs)
        ppr = paragraph.find("w:pPr", NS)
        style = ""
        level = None
        if ppr is not None:
            pstyle = ppr.find("w:pStyle", NS)
            if pstyle is not None:
                style = self.styles.get(pstyle.get(q("val")), pstyle.get(q("val")))
            outline = ppr.find("w:outlineLvl", NS)
            if outline is not None:
                level = int(outline.get(q("val"))) + 1
        heading = re.match(r"(?i)heading\s*(\d)", style)
        if heading:
            level = int(heading.group(1))
        if re.match(r"(?i)^title$", style):
            level = 1
        if not text:
            return notes
        if level and level <= 6:
            counters.clear()
            return ["", "#" * level + " " + text.replace("**", ""), ""] + notes
        numpr = ppr.find("w:numPr", NS) if ppr is not None else None
        if numpr is not None:
            ilvl_el = numpr.find("w:ilvl", NS)
            num_el = numpr.find("w:numId", NS)
            ilvl = ilvl_el.get(q("val")) if ilvl_el is not None else "0"
            num_id = num_el.get(q("val")) if num_el is not None else "0"
            fmt = self.numbering.get(num_id, {}).get(ilvl, "bullet")
            indent = "  " * int(ilvl)
            if fmt in ("bullet", "none"):
                return [f"{indent}- {text}"] + [indent + "  " + n for n in notes]
            key = (num_id, ilvl)
            counters[key] = counters.get(key, 0) + 1
            return [f"{indent}{counters[key]}. {text}"] + [indent + "   " + n for n in notes]
        counters.clear()
        return ["", text] + notes

    def table(self, table):
        rows, notes = [], []
        for tr in table.findall("w:tr", NS):
            cells = []
            for tc in tr.findall("w:tc", NS):
                texts = []
                for p in tc.iter(q("p")):
                    text, refs = self.runs(p)
                    notes.extend(self.comment_lines(refs))
                    if text:
                        texts.append(text)
                cells.append("<br>".join(texts).replace("|", "\\|"))
            if any(cells):
                rows.append(cells)
        if not rows:
            return notes
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        out = ["", "| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
        out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        return out + [""] + notes

    def body(self, root):
        lines, counters = [], {}
        for element in root.find("w:body", NS):
            if element.tag == q("p"):
                lines += self.paragraph(element, counters)
            elif element.tag == q("tbl"):
                counters.clear()
                lines += self.table(element)
            elif element.tag == q("sdt"):
                content = element.find("w:sdtContent", NS)
                for p in (content if content is not None else []):
                    if p.tag == q("p"):
                        lines += self.paragraph(p, counters)
        rest = [k for k in self.comments if k not in self.used_comments]
        if rest:
            lines += ["", "## Comments without an anchor", ""]
            lines += [f"> **Comment ({self.comments[k][0]}):** {self.comments[k][1]}" for k in rest]
        text = "\n".join(lines)
        return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    source = Path(args[0])
    target = Path(args[1]) if len(args) > 1 else source.with_suffix(".md")
    with zipfile.ZipFile(source) as archive:
        converter = Converter(archive, keep_strike="--keep-strike" in argv)
        markdown = converter.body(read_xml(archive, "word/document.xml"))
    target.write_text(markdown, encoding="utf-8")
    print(f"written {target}: {len(markdown.splitlines())} lines, "
          f"{len(converter.comments)} comments, {converter.dropped_strike} struck-through runs dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
