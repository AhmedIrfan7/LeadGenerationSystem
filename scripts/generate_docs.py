"""Generates the project documentation PDF. Run: python scripts/generate_docs.py"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    ListFlowable, ListItem, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase.pdfmetrics import stringWidth

INK = colors.HexColor("#0f172a")
ACCENT = colors.HexColor("#4f46e5")
MUTED = colors.HexColor("#64748b")
LIGHT_BG = colors.HexColor("#f1f5f9")
LINE = colors.HexColor("#cbd5e1")

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="CoverTitle", fontName="Helvetica-Bold", fontSize=28, leading=34,
    textColor=INK, alignment=TA_CENTER, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="CoverSubtitle", fontName="Helvetica", fontSize=14, leading=20,
    textColor=MUTED, alignment=TA_CENTER, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="CoverMeta", fontName="Helvetica", fontSize=10.5, leading=16,
    textColor=MUTED, alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    name="H1", fontName="Helvetica-Bold", fontSize=17, leading=22,
    textColor=INK, spaceBefore=18, spaceAfter=10
))
styles.add(ParagraphStyle(
    name="H2", fontName="Helvetica-Bold", fontSize=12.5, leading=17,
    textColor=ACCENT, spaceBefore=14, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="Body", fontName="Helvetica", fontSize=10.2, leading=15.5,
    textColor=INK, spaceAfter=8, alignment=TA_LEFT
))
styles.add(ParagraphStyle(
    name="BodySmall", fontName="Helvetica", fontSize=9.3, leading=13.6,
    textColor=MUTED, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="BulletItem", fontName="Helvetica", fontSize=10.2, leading=15,
    textColor=INK, spaceAfter=3
))
styles.add(ParagraphStyle(
    name="PlaceholderText", fontName="Helvetica-Bold", fontSize=10, leading=14,
    textColor=INK, alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    name="TocEntry", fontName="Helvetica", fontSize=10.5, leading=20,
    textColor=INK
))
styles.add(ParagraphStyle(
    name="Caption", fontName="Helvetica-Oblique", fontSize=8.8, leading=12,
    textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10
))


def placeholder(label, height=6.0):
    """A bordered box marking where a screenshot goes, plus a caption below it."""
    t = Table([[Paragraph(f"ADD SCREENSHOT HERE:<br/>{label}", styles["PlaceholderText"])]],
              colWidths=[16.2 * cm], rowHeights=[height * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 1, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def divider():
    return HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=2, spaceAfter=14)


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(i, styles["BulletItem"]), bulletColor=ACCENT) for i in items],
        bulletType="bullet", start="circle", leftIndent=14, spaceBefore=2, spaceAfter=10
    )


def feature_table(rows):
    data = [[Paragraph(f"<b>{a}</b>", styles["Body"]), Paragraph(b, styles["Body"])] for a, b in rows]
    t = Table(data, colWidths=[5.0 * cm, 11.2 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


story = []

# ---------------- Cover page ----------------
story.append(Spacer(1, 6.5 * cm))
story.append(Paragraph("Automated Lead Generation System", styles["CoverTitle"]))
story.append(Paragraph("From a spreadsheet row to a live, deployed website and a client email, with no manual steps in between.", styles["CoverSubtitle"]))
story.append(Spacer(1, 1.2 * cm))
story.append(HRFlowable(width="40%", thickness=1, color=ACCENT, hAlign="CENTER", spaceAfter=14))
story.append(Paragraph("Prepared by Ahmed Irfan", styles["CoverMeta"]))
story.append(Paragraph("AI &amp; Automation Team", styles["CoverMeta"]))
story.append(Paragraph("Live application: lead-generation-system-by-ahmed-irfan.vercel.app", styles["CoverMeta"]))
story.append(Paragraph("Source repository: github.com/AhmedIrfan7/LeadGenerationSystem", styles["CoverMeta"]))
story.append(PageBreak())

# ---------------- Table of contents ----------------
story.append(Paragraph("Table of Contents", styles["H1"]))
story.append(divider())
toc_items = [
    "1. Executive Summary",
    "2. What This System Does",
    "3. Why This Approach",
    "4. How It Works: The User Journey",
    "5. System Architecture",
    "6. The Four Workflows",
    "7. The Dashboard",
    "8. Reliability and Error Handling",
    "9. Security and Credential Handling",
    "10. Technology Stack",
    "11. Deployment",
    "12. What Was Tested",
    "13. Possible Next Steps",
    "14. Conclusion",
]
for item in toc_items:
    story.append(Paragraph(item, styles["TocEntry"]))
story.append(PageBreak())

# ---------------- 1. Executive Summary ----------------
story.append(Paragraph("1. Executive Summary", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "This system automates the entire process of turning a list of prospect websites into redesigned, "
    "live preview sites that are sent directly to each client, with zero manual work beyond adding a "
    "row to a spreadsheet. It was built as a production grade automation pipeline using n8n for "
    "orchestration, OpenAI for content and design generation, GitHub for hosting, and a custom web "
    "dashboard for monitoring and control.", styles["Body"]))
story.append(Paragraph(
    "The team's only remaining task is pasting a website URL and a client email into a Google Sheet. "
    "Everything else, scraping the prospect's current site, generating a redesigned version, deploying "
    "it live, and emailing the client the link, happens automatically. The system also includes a live "
    "dashboard so progress and results can be monitored in real time, and a manual trigger for on-demand "
    "runs when instant results are needed.", styles["Body"]))
story.append(Paragraph(
    "This document explains what the system does, how it was built, the engineering decisions behind it, "
    "and how it can be operated and extended going forward.", styles["Body"]))

# ---------------- 2. What This System Does ----------------
story.append(Paragraph("2. What This System Does", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "In one sentence: it converts a spreadsheet of prospect websites into deployed, redesigned preview "
    "sites and automatically emails each client a link to theirs.", styles["Body"]))
story.append(Paragraph("At a high level, for every lead added to the sheet, the system:", styles["Body"]))
story.append(bullets([
    "Scrapes the prospect's existing website content (homepage plus relevant internal pages such as About, Services, or Contact).",
    "Sends that content to an AI model, which produces a full redesign: business name, tagline, color palette, and page sections.",
    "Renders that design into a real, modern, mobile responsive static website (HTML and CSS).",
    "Creates a new GitHub repository for that client and deploys the site live using GitHub Pages.",
    "Emails the client a professional message containing the live preview link.",
    "Updates the spreadsheet with the outcome: status, live URL, and timestamp, all visible on a live dashboard.",
]))

# ---------------- 3. Why This Approach ----------------
story.append(Paragraph("3. Why This Approach", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "The brief asked for a fully automated, production level system focused on scalability, reliability, "
    "and clean execution. Every major design decision was made with those three goals in mind.", styles["Body"]))
story.append(feature_table([
    ("Scalability", "Each lead is processed as its own isolated unit of work. Adding more leads to the "
                     "sheet does not require any change to the system, and one lead's failure never blocks another."),
    ("Reliability", "Every external call (scraping, AI, GitHub, email) has retry logic. GitHub operations are "
                     "idempotent, meaning the system can safely retry a failed lead without creating duplicate "
                     "repositories or sending duplicate emails."),
    ("Clean execution", "Failures are never silent. Expected failures (a site being down, malformed AI output) "
                         "resolve to a clear status in the sheet with a human readable error message. Unexpected "
                         "crashes trigger a separate admin alert so nothing goes unnoticed."),
]))

# ---------------- 4. How It Works ----------------
story.append(PageBreak())
story.append(Paragraph("4. How It Works: The User Journey", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "The only manual step in the entire system is adding a row to the Leads spreadsheet with a website "
    "URL and a client email address. From that point on, the pipeline runs itself.", styles["Body"]))
story.append(Paragraph("Step by step:", styles["H2"]))
story.append(bullets([
    "<b>Step 1, a lead is added.</b> A team member pastes a website URL and client email into the sheet. No other field needs to be filled in.",
    "<b>Step 2, the system checks for new leads.</b> This happens automatically on a schedule, and can also be triggered instantly from the dashboard's Run Now button.",
    "<b>Step 3, the site is scraped.</b> The prospect's homepage and a couple of relevant internal pages are read to understand what the business does.",
    "<b>Step 4, the AI designs a new site.</b> The scraped content is sent to OpenAI, which returns a structured redesign: business name, tagline, a color palette, and page sections such as hero, about, services, testimonials, and contact.",
    "<b>Step 5, the website is built.</b> That structured design is turned into a real, working website, styled and responsive, with no manual coding involved.",
    "<b>Step 6, the website goes live.</b> A new GitHub repository is created for the client and the site is deployed instantly using GitHub Pages, giving it a real, working public URL.",
    "<b>Step 7, the client is emailed.</b> A professional email is sent automatically with a button linking to their new live preview site.",
    "<b>Step 8, the record is updated.</b> The spreadsheet and the live dashboard both reflect the final result: status, live link, and timestamp.",
]))

# ---------------- 5. System Architecture ----------------
story.append(PageBreak())
story.append(Paragraph("5. System Architecture", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "The system is built from four independent n8n workflows that each do one job well, plus a web "
    "dashboard that reads from them. This separation is a deliberate engineering choice: it means a "
    "problem in one part of the system (for example, one client's website being unreachable) can never "
    "bring down the rest of the pipeline.", styles["Body"]))
story.append(feature_table([
    ("Lead-Gen Orchestrator", "Watches the spreadsheet for new or retried leads, hands each one off "
                               "individually, and writes the final result back."),
    ("Process Single Lead", "Does the real work for exactly one lead: scrape, generate, build, deploy, email."),
    ("Error Notifier", "A safety net. If anything crashes in a way the other workflows did not already "
                        "handle gracefully, this alerts an administrator immediately by email."),
    ("Dashboard API", "A small set of endpoints that let the web dashboard read live lead data and trigger "
                       "retries or on-demand runs, without giving the dashboard direct access to the spreadsheet."),
]))

# ---------------- 6. The Four Workflows ----------------
story.append(PageBreak())
story.append(Paragraph("6. The Four Workflows", styles["H1"]))
story.append(divider())

story.append(Paragraph("6.1 Lead-Gen Orchestrator", styles["H2"]))
story.append(Paragraph(
    "Runs automatically once every 24 hours, and can also be triggered instantly at any time from the "
    "dashboard's Run Now button. It reads the spreadsheet, filters for rows that are new or marked for "
    "retry, and dispatches each one to the Process Single Lead workflow. Once that finishes, it writes "
    "the outcome, success or failure, back to the sheet.", styles["Body"]))

story.append(Paragraph("6.2 Process Single Lead", styles["H2"]))
story.append(Paragraph(
    "The core of the system. Every step described in section 4 (scraping, AI generation, site building, "
    "GitHub deployment, and emailing the client) happens inside this workflow, once per lead. It is built "
    "so that every step can fail safely: a bad website, a malformed AI response, or a temporary GitHub "
    "error all resolve into a clear, specific error message rather than a silent failure.", styles["Body"]))

story.append(Paragraph("6.3 Error Notifier", styles["H2"]))
story.append(Paragraph(
    "A dedicated safety-net workflow. It is registered as the official error handler for the two workflows "
    "above, so any uncaught technical failure anywhere in the pipeline immediately emails an administrator "
    "with the workflow name, the exact step that failed, and a direct link to the failed run.", styles["Body"]))

story.append(Paragraph("6.4 Dashboard API", styles["H2"]))
story.append(Paragraph(
    "Provides the endpoints the web dashboard uses: one to fetch the current list of leads and their "
    "status, one to let a team member manually retry a failed lead, and one to trigger an on-demand run "
    "of the whole pipeline. This keeps the spreadsheet credentials on the automation side only, the "
    "dashboard never touches the spreadsheet directly.", styles["Body"]))

# ---------------- 7. The Dashboard ----------------
story.append(PageBreak())
story.append(Paragraph("7. The Dashboard", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "A live web application built to give visibility into the pipeline without needing to open n8n or the "
    "spreadsheet directly. It is live at lead-generation-system-by-ahmed-irfan.vercel.app and updates "
    "automatically every ten seconds.", styles["Body"]))
story.append(bullets([
    "<b>Status overview.</b> At a glance counts of how many leads are pending, processing, done, or failed.",
    "<b>Full leads table.</b> Every lead with its website, client details, current status, and live link once ready.",
    "<b>One click retry.</b> Any failed lead can be retried directly from the dashboard, no need to edit the spreadsheet.",
    "<b>Run Now button.</b> Instantly triggers the pipeline to check for new leads, instead of waiting for the automatic schedule.",
]))

# ---------------- 8. Reliability and Error Handling ----------------
story.append(PageBreak())
story.append(Paragraph("8. Reliability and Error Handling", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "Reliability was treated as a first class requirement, not an afterthought. Several concrete "
    "engineering decisions make the system resilient in practice, not just in theory.", styles["Body"]))
story.append(feature_table([
    ("Idempotent operations", "GitHub repository creation, file uploads, and page publishing all check "
                               "existing state first. Retrying a lead never creates duplicates."),
    ("Automatic retries", "Every network call has bounded retry logic, so a brief network blip does not "
                           "fail an entire lead."),
    ("Self healing writes", "If two updates to the same file conflict, the system automatically re-checks "
                             "the current state and retries the write, rather than failing outright."),
    ("Two tier error handling", "Expected failures (a site being down, an AI response being invalid) "
                                 "produce a clear status and message in the spreadsheet. Unexpected crashes "
                                 "trigger a separate, immediate email alert to an administrator."),
    ("Per lead isolation", "Every lead is processed independently, so one problematic website can never "
                            "block or slow down the rest of the batch."),
]))

# ---------------- 9. Security and Credential Handling ----------------
story.append(Paragraph("9. Security and Credential Handling", styles["H1"]))
story.append(divider())
story.append(bullets([
    "All third party credentials (Google Sheets, OpenAI, GitHub, Gmail) are stored securely inside n8n's "
    "credential manager and are never exposed in workflow logic or in the dashboard.",
    "The dashboard communicates only with a small set of purpose built endpoints. It has no direct access "
    "to the spreadsheet, GitHub, or email credentials.",
    "All AI generated and scraped content is sanitized before being inserted into the generated websites, "
    "preventing malicious content from being injected into a client's page.",
]))

# ---------------- 10. Technology Stack ----------------
story.append(Paragraph("10. Technology Stack", styles["H1"]))
story.append(divider())
story.append(feature_table([
    ("Automation", "n8n Cloud, running four connected workflows"),
    ("AI generation", "OpenAI Chat Completions API for content and design generation"),
    ("Hosting", "GitHub REST API for repository creation and file deployment, GitHub Pages for live hosting"),
    ("Email", "Gmail, for both client delivery and internal admin alerts"),
    ("Data source", "Google Sheets, acting as the single source of truth for every lead"),
    ("Dashboard", "Next.js, TypeScript, and Tailwind CSS, deployed on Vercel"),
]))

# ---------------- 11. Deployment ----------------
story.append(PageBreak())
story.append(Paragraph("11. Deployment", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "The automation layer runs continuously on n8n Cloud. The dashboard is deployed on Vercel and is "
    "publicly live at:", styles["Body"]))
t = Table([[Paragraph("lead-generation-system-by-ahmed-irfan.vercel.app", styles["PlaceholderText"])]],
          colWidths=[16.2 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef2ff")),
    ("BOX", (0, 0), (-1, -1), 1, ACCENT),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))
story.append(t)
story.append(Spacer(1, 10))
story.append(Paragraph(
    "The full source code, including all four n8n workflow files and the dashboard application, is version "
    "controlled and available at github.com/AhmedIrfan7/LeadGenerationSystem, built and committed in "
    "fifty incremental, individually verified steps.", styles["Body"]))

# ---------------- 12. What Was Tested ----------------
story.append(Paragraph("12. What Was Tested", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "The system was validated in two ways before being considered complete: automated structural "
    "validation of every workflow, and live end to end testing with a real website and a real email "
    "delivery.", styles["Body"]))
story.append(bullets([
    "An automated validation script checks every workflow file for structural correctness and confirms "
    "every step is properly connected, with no missing or dead end steps.",
    "A real lead was run through the complete pipeline live: the website was scraped, a new design was "
    "generated, a live site was deployed to GitHub Pages, and a real email was received with the working link.",
    "Failure scenarios were deliberately tested, including unreachable websites and write conflicts, to "
    "confirm the system fails safely and recovers automatically where possible.",
]))

# ---------------- 13. Possible Next Steps ----------------
story.append(PageBreak())
story.append(Paragraph("13. Possible Next Steps", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "The system is complete and production ready as specified. If the team wants to extend it further, "
    "natural next steps include:", styles["Body"]))
story.append(bullets([
    "Custom domain support for client sites, instead of the default GitHub Pages address.",
    "A simple approval step so a team member can preview a generated site before the client email is sent.",
    "Analytics on generated sites, such as link clicks, to measure client engagement.",
    "Support for additional AI generated design templates, giving each client's site more visual variety.",
]))

# ---------------- 14. Conclusion ----------------
story.append(Paragraph("14. Conclusion", styles["H1"]))
story.append(divider())
story.append(Paragraph(
    "This system delivers exactly what was asked for: a fully automated, production grade lead generation "
    "pipeline that requires no manual steps beyond adding a lead to a spreadsheet, built with scalability, "
    "reliability, and clean execution as core design principles throughout. It is live, tested, documented, "
    "and ready for real client use today.", styles["Body"]))

doc = SimpleDocTemplate(
    "generated_docs/LeadGenerationSystem_Documentation.pdf",
    pagesize=A4,
    topMargin=2.2 * cm, bottomMargin=2.2 * cm,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    title="Automated Lead Generation System",
    author="Ahmed Irfan",
)
doc.build(story)
print("PDF generated.")
