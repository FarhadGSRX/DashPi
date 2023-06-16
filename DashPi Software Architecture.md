
```dataviewjs
// Fill in the below script template

let script = {
  "name": "~/main.py",
  "docstring": "The Docstring",
  "imports": "The Imports",
  "setup": "The Script Setup",
  "functions": [
    {
      "fxn_name": "main",
      "fxn_params": [
        {
          "param_name": "Parameter Name",
          "param_type": "Parameter Type",
          "param_hint": "Parameter Hint/Description"
        }
      ],
      "fxn_output": {
        "output_type": "Output Variable Type",
        "output_hint": "Output Hint/Description"
      },
      "fxn_docstring": "The Function Docstring"
    }
  ],
  "main": {
    "main_docstring": "If-Main Docstring"
  }
}

await dv.view("zMeta/_Control/JS_Views/code_schema", script)
```
