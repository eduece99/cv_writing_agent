# CV and Cover Letter Generator

Writes a CV and Cover Letter from a supplied bio or profile, against a job description

This should be self explanatory and a lot more detail is in the `copilot-instructions.md` file

However, there are some summary points: 

Everything produced goes into the `output` folder

Your 4 input files go into the `ref` folder, ideally named:
- `cv_template.docx`
- `cl_template.docx` (covering letter)
- `bio.txt`
- `job_description.txt`

**Example prompt** - ```
Please write me a CV and covering letter relating to the job description in this URL - [URL] using the files "cv_template.docx", "cl_template.docx", and "Profile.pdf" in the "ref" folder
```

Other file formats besides .txt and .docx are allowed.  The agent should ask you about this.

Good luck!
