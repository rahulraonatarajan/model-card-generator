
#!/usr/bin/env python3
"""
Model Card Generator
====================
Quickly generate a Markdown model-card file for any local or Hugging Face-style model directory.
(Full docstring shortened for brevity in this example.)
"""
import argparse, datetime
from pathlib import Path
from typing import Dict, Any
try:
    from transformers import AutoConfig
except ImportError:
    AutoConfig = None
try:
    from jinja2 import Template
except ImportError:
    Template = None

DEFAULT_TEMPLATE = """# {{ model_name }}
**Model Card generated on {{ date }}**
## Overview
- **Base model / architecture**: {{ architecture | default('N/A') }}
- **Number of parameters**: {{ num_params | default('N/A') }}
- **License**: {{ license | default('N/A') }}
- **Author / Organization**: {{ author | default('Unknown') }}
- **Intended use**:
  {{ intended_use | default('Describe intended applications here') }}
- **Limitations**:
  {{ limitations | default('Describe known limitations and biases') }}

## Training Data
{{ training_data | default('Description of datasets and preprocessing') }}

## Evaluation
{{ evaluation | default('Metrics, benchmarks, results') }}

## Ethical Considerations
{{ ethical_considerations | default('Potential risks, misuses, fairness concerns') }}

## Citation
If you use this model, please cite:
```
@software{ {{ model_name|replace(' ','_') }},
  title={{ "{{ model_name }}" }},
  author={{ "{{ author | default('Unknown') }}" }},
  year={{ year }}
}
```
"""

def gather_metadata(model_path:str, interactive:bool=False)->Dict[str,Any]:
    meta:Dict[str,Any]={}
    cfg_path=Path(model_path)
    if AutoConfig and cfg_path.exists():
        try:
            cfg=AutoConfig.from_pretrained(str(cfg_path))
            meta["model_name"]=cfg.name_or_path
            meta["architecture"]=(cfg.architectures[0]
                if hasattr(cfg,"architectures") and cfg.architectures else "Unknown")
            meta["num_params"]=getattr(cfg,"num_parameters", "N/A")
            meta["license"]=getattr(cfg,"license", None)
        except Exception as e:
            print(f"[WARN] Could not load config: {e}")
    if interactive:
        for field, prompt in {
            "author":"Author or organization",
            "intended_use":"Intended use cases",
            "limitations":"Known limitations or biases",
            "training_data":"Description of training data",
            "evaluation":"Evaluation details",
            "ethical_considerations":"Ethical considerations",
        }.items():
            default=meta.get(field,"")
            response=input(f"{prompt}{f' [{default}]' if default else ''}: ") or default
            meta[field]=response
    meta.setdefault("model_name", Path(model_path).name)
    return meta

def render_card(meta:Dict[str,Any], template_str:str=DEFAULT_TEMPLATE)->str:
    meta={**meta,"date":datetime.date.today().isoformat(),"year":datetime.date.today().year}
    if Template:
        return Template(template_str).render(**meta)
    from string import Template as StrTemplate
    simple_template=template_str.replace("{{ model_name }}","${model_name}")
    return StrTemplate(simple_template).substitute(meta)

def main()->None:
    p=argparse.ArgumentParser(description="Generate a Markdown model card.")
    p.add_argument("--model_path", required=True)
    p.add_argument("--output", default="MODEL_CARD.md")
    p.add_argument("--template")
    p.add_argument("--interactive", action="store_true")
    args=p.parse_args()
    tmpl=Path(args.template).read_text() if args.template else DEFAULT_TEMPLATE
    meta=gather_metadata(args.model_path, args.interactive)
    card=render_card(meta, tmpl)
    Path(args.output).write_text(card, encoding="utf-8")
    print(f"[INFO] Model card written to {args.output}")
if __name__=="__main__": main()
