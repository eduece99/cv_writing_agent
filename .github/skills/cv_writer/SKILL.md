---
name: cv_writer
description: "Use when writing a Curriculum Vitae (Resume), ideally from a supplied template, job description, and candidate bio.   The CV should be professionally formatted and tailored to the job or industry being targeted, based on the bio."
---


# Output Files
- *Generated CV*: a single file: `cv.docx`.  

# Writing Guidelines

The *Generated CV* should be written in a professional style, with clear sections for personal information, education, work experience, skills, and references. The content should be concise, relevant, and tailored to the job or industry being targeted. The document should be formatted for readability and visual appeal, using appropriate fonts, headings, and spacing.

The *Generated CV* should be generated based on the *Candidate Bio* and *Job Description*, and should adhere to the formatting and style guidelines of the *CV Template*. The agent should ensure that the generated CV is tailored to the job or industry being targeted, and that it highlights the candidate's relevant skills and experience.

Font should be professional and easy to read, such as Arial, Calibri, or Times New Roman.  Font size should be between 10-12 points for the main text, and larger for headings.  Headings should be clear and consistent throughout the document, using bold or italic formatting as appropriate.  Spacing should be consistent, with adequate white space to enhance readability.  Margins should be set to standard sizes (1 inch on all sides) to ensure that the document is well-balanced and visually appealing.

The CV, unless specified by the user, should be two pages long in length, and should include the following sections:
- Personal Information: Name, contact information, and a professional summary or objective statement.
- Education: List of degrees, institutions, and graduation dates.
- Work Experience: List of relevant work experience, including job titles, company names, dates of employment, and a brief description of responsibilities and achievements.
- Skills: List of relevant skills, including technical skills, soft skills, and any certifications or licenses.

References are not necessary to include in the CV, but if the user requests them, they should be included in a separate section at the end of the CV.


Please do not lie or make up things.  Nothing should be written in the *Generated CV* that is not supported by the *Candidate Bio*.  If the agent is unsure about any information, it should ask the user for clarification before proceeding.  In addition, doubtful areas *should be marked on the CV* with a comment, so that the user can review and provide clarification.  The agent should not make assumptions about the user's intent, and should always seek clarification when in doubt.

Finally, please put the following at the end of the CV file in a smaller font (e.g. font sizes 8 or 10): "This CV was generated with the use of an AI assistant [insert model name here] and thereafter proof-read.  Please visit my github for details."