# Copilot agent instructions

## Project at a glance

This is an agentic project which is not programming-language centered.  The aim is to write a Curriculum Vitae (Resume in American English) and a covering letter in .docx format, or .pdf if not possible.  They should be written in a professional style, with clear sections for personal information, education, work experience, skills, and references. The content should be concise, relevant, and tailored to the job or industry being targeted. The document should be formatted for readability and visual appeal, using appropriate fonts, headings, and spacing.  


# Prerequisite Files

Any agent should check for the existence of the following files in the `ref` directory before proceeding:

- *CV Template*: A template should be provided by the user, ideally named `cv_template.docx`, which will be used to generate the final CV. The agent should ensure that the generated CV adheres to the template's formatting and style guidelines.
- *Letter Template*: A template should be provided by the user, ideally named `cl_template.docx`, which will be used to generate the final covering letter. 
- *Candidate Bio*: a bio of the candidate, ideally named `bio.txt` or `bio.docx` or `bio.pdf`, which will be used to generate the final CV. The agent should ensure that the generated CV adheres to the template's formatting and style guidelines.  One example could be the candidate's LinkedIn profile, which can be used to extract relevant information for the CV and covering letter.  The agent should ensure that the generated CV adheres to the template's formatting and style guidelines.
- *Job Description*: a job description, ideally named `job_description.txt` or `job_description.docx`, which will be used to generate the final CV.  If no job description file is provided, a URL to a web page can be presented.  The agent should ensure that the generated CV adheres to the template's formatting and style guidelines.  There should be a requirements section in the job description, which will be used to generate the final CV. 


These files, where applicable, are elaborated in the SKILL.MD files for more specifics (especially naming and formatting), and should be present in the tracked repository or working directory before proceeding.  The agent should ensure that the generated CV adheres to the template's formatting and style guidelines.

If they do not exist, or if the agent is unsure about any information, it should ask the user for clarification before proceeding.  In addition, doubtful areas *should be marked on the CV* with a comment and also written in the report, so that the user can review and provide clarification.  The agent should not make assumptions about the user's intent, and should always seek clarification when in doubt.

# Output Files
- *Generated CV*: a single file: `output/[datetime]/cv_autogen.docx`.  
- *Generated Letter*: a single file: `output/[datetime]/cl_autogen.docx`.
- *Report*: a single file: `output/[datetime]/report.txt`.  This file should contain a summary of the process, including key deviations from the template(s), any issues encountered, any assumptions made, and any areas where clarification was needed from the user.  The report should also include a summary of the candidate's qualifications and how they align with the job requirements giving a score from 1-10 (10 is perfect alignment, 1 is no alignment whatsoever), as well as any recommendations for further action.
- *AGENTS.MD*: a single file: `./AGENTS.MD`.  This file should contain any information that would accelerate future runs of the agents, such as recommended software to be used.  More info in *Shortcuts* section below.

[datetime] should be replaced with the current date and time in the format `YYYYMMDD_HHMMSS`, e.g., `20230401_153000`.  The agent should ensure that the generated CV adheres to the template's formatting and style guidelines.

# Writing Guidelines

Please do not lie or make up things.  Nothing should be written in the *Generated CV* and *Generate Letter* that is not supported by the *Candidate Bio*.  If the agent is unsure about any information, it should ask the user for clarification before proceeding.  In addition, doubtful areas *should be marked on the CV* with a comment, so that the user can review and provide clarification.  The agent should not make assumptions about the user's intent, and should always seek clarification when in doubt.

# Shortcuts

Anything that the agent can do to make the process easier for the user should be done.  For example, if the user provides a URL to a web page, the agent should extract relevant information from the web page and use it to generate the CV and covering letter.  If the user provides a LinkedIn profile, the agent should extract relevant information from the profile and use it to generate the CV and covering letter.  The agent should also be able to handle different file formats, such as .docx, .pdf, .txt, and .md.

This is likely a repetetive process and the user will ask for multiple iterations of the CV and covering letter.  The agent should be able to handle this and make the process as smooth as possible for the user.  The agent should also be able to handle different file formats, such as .docx, .pdf, .txt, and .md.  

Of note, it is recommended that files be saved in this workspace that may guide future runs of the agents, such as recommended software to be used.  A suggested filename for pointers would be `AGENTS.MD` which can be used to store information that would accelerate future runs of the agents.  This file should be updated with any new information that would be useful for future runs of the agents, such as recommended software to be used.  The agent should ensure that the generated CV adheres to the template's formatting and style guidelines.  

If this file does not exist, please create the file.

# Software

As usual.  Please ask the user when new software is to be installed.  This must be open source software.  

No new python environments should be created unless absolutely necessary.

