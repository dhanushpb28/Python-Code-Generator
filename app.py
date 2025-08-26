# app.py
import re
import textwrap
from flask import Flask, request, render_template_string

app = Flask(__name__)

CODE_TEMPLATES = {
    "phone": textwrap.dedent("""\
        import re

        input_string = {input_string_literal}
        pattern = r'(?<!\\d)[6-9]\\d{{9}}(?!\\d)' 

        matches = re.findall(pattern, input_string)

        if matches:
            for phone_number in matches:
                print(f"Extracted Phone Number: {{phone_number}}")
        else:
            print("No phone number found.")
    """),

    "email": textwrap.dedent("""\
        import re

        input_string = {input_string_literal}
        pattern = r'[\\w.+-]+@[\\w-]+\\.[\\w.-]+' 

        matches = re.findall(pattern, input_string)

        if matches:
            for email in matches:
                print(f"Extracted Email: {{email}}")
        else:
            print("No email found.")
    """),

    "url": textwrap.dedent("""\
        import re

        input_string = {input_string_literal}
        pattern = r'https?://\\S+'  

        matches = re.findall(pattern, input_string)

        if matches:
            for url in matches:
                print(f"Extracted URL: {{url}}")
        else:
            print("No URL found.")
    """),

    "remove_html": textwrap.dedent("""\
        import re

        input_string = {input_string_literal}
        clean_text = re.sub(r'<.*?>', '', input_string) 

        print("Text without HTML tags:", clean_text)
    """),
}


HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Python Code Generator</title>
  <style>
    body { 
      font-family: system-ui, sans-serif; 
      margin: 0; 
      min-height: 100vh;
      display: flex; 
      justify-content: center; 
      align-items: flex-start; 
      padding: 2rem;
      color:#111; 
      background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #a1c4fd, #c2e9fb);
      background-size: 400% 400%;
      animation: gradientBG 12s ease infinite;
    }
    @keyframes gradientBG {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    h2 { font-size: 1.6rem; margin-bottom: 1rem; text-align:center; }
    .container { max-width: 700px; margin: auto; background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); }
    textarea { width: 100%; padding:12px; font-size:15px; border-radius:8px; border:1px solid #ccc; margin-bottom:15px; resize: vertical; }
    .task-options { display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem; }
    .task-option { background:#fff; border:1px solid #ddd; padding:10px 14px; border-radius:8px; cursor:pointer; transition: all 0.2s; }
    .task-option input { margin-right: 8px; }
    .task-option:hover { background:#f0f0f0; border-color:#007bff; }
    .submit-btn { padding:12px 20px; border-radius:8px; background:#007bff; color:#fff; border:none; cursor:pointer; font-size:15px; transition: background 0.2s; }
    .submit-btn:hover { background:#0056b3; }
    .results, .code-block { margin-top: 2rem; }
    pre { position: relative; background:#2d2d2d; color:#f8f8f2; padding:14px; border-radius:10px; overflow:auto; white-space:pre-wrap; font-size:14px; }
  </style>
</head>
<body>
<div class="container">
  <h2>Python Code Generator</h2>
  <form method="post">
    <textarea name="user_input" placeholder="Enter your text here...">{{ input_text }}</textarea>
    <div class="task-options">
      <label class="task-option"><input type="radio" name="task" value="phone" {% if selected_task=="phone" %}checked{% endif %}>📱 Phone Numbers</label>
      <label class="task-option"><input type="radio" name="task" value="email" {% if selected_task=="email" %}checked{% endif %}>📧 Emails</label>
      <label class="task-option"><input type="radio" name="task" value="url" {% if selected_task=="url" %}checked{% endif %}>🌍 URLs</label>
      <label class="task-option"><input type="radio" name="task" value="remove_html" {% if selected_task=="remove_html" %}checked{% endif %}>🧹 Remove HTML Tags</label>
    </div>
    <input type="submit" class="submit-btn" value="Generate Python Code">
  </form>

  {% if results %}
    <div class="results">
      <h3>Results:</h3>
      <p>{{ results | join(', ') }}</p>
    </div>
  {% endif %}

  {% if generated_code %}
    <div class="code-block">
      <h3>Generated Python Code:</h3>
      <pre><code id="codeBox">{{ generated_code }}</code></pre>
    </div>
  {% endif %}
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    generated_code = ""
    input_text = ""
    results = []
    selected_task = "phone"

    if request.method == 'POST':
        input_text = request.form.get('user_input', '').strip()
        selected_task = request.form.get('task', 'phone')

        if input_text and selected_task in CODE_TEMPLATES:
            if selected_task == "phone":
                pattern = r'(?<!\d)[6-9]\d{9}(?!\d)'
                results = re.findall(pattern, input_text)
            elif selected_task == "email":
                pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'
                results = re.findall(pattern, input_text)
            elif selected_task == "url":
                pattern = r'https?://\S+'
                results = re.findall(pattern, input_text)
            elif selected_task == "remove_html":
                results = [re.sub(r'<.*?>', '', input_text)]

            generated_code = CODE_TEMPLATES[selected_task].format(
                input_string_literal=repr(input_text)
            )
        elif input_text:
            generated_code = "# No results found for the selected task."

    return render_template_string(
        HTML_TEMPLATE,
        generated_code=generated_code,
        input_text=input_text,
        results=results,
        selected_task=selected_task
    )

if __name__ == '__main__':
    app.run(debug=True)

