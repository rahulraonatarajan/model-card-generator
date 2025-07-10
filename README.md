# Model Card Generator – GitHub Action

**Version:** 2025-07-09

Automatically create or update a `MODEL_CARD.md` for any Transformer-style model directory in your repository. The Action wraps an easy-to-use Python script that relies on **`transformers`**, **`torch`**, and **`jinja2`**.

---

## Quick Start

1. Copy the composite Action folder to `.github/actions/model-card-generator/` (included in this repo).
2. Add the sample workflow at `.github/workflows/generate-model-card.yml`.
3. Commit & push. A fresh **MODEL_CARD.md** appears on every push that modifies your model files.

```yaml
# .github/workflows/generate-model-card.yml (excerpt)
- name: Run Model Card Generator Action
  uses: ./.github/actions/model-card-generator
  with:
    model_path: './my_model'
    output: 'MODEL_CARD.md'
```

---

## Why Model Cards?

Model cards promote transparency and responsible AI by documenting:

* Architecture & parameter count
* Intended use and limitations
* Training data & evaluation metrics
* Ethical considerations

<sub>Inspired by Google’s Model Cards framework.</sub>

---

## Local CLI

```bash
python model_card_generator.py --model_path ./my_model --interactive
```

The `--interactive` flag will prompt you for missing metadata such as _Intended Use_ or _Ethical Considerations_.

---

## Example Output

Below is a real **MODEL_CARD.md** generated for a fictional TinyLlama-1.1B checkpoint. It shows the default Markdown template filled with metadata auto-extracted from `config.json` plus a few interactive answers:

```markdown
# TinyLlama-1.1B

**Model Card generated on 2025-07-09**

## Overview
- **Base model / architecture**: LLaMAForCausalLM
- **Number of parameters**: 1.1 B
- **License**: MIT
- **Author / Organization**: TinyLlama project
- **Intended use**:
  Lightweight, on-device conversational AI for low-resource environments.
- **Limitations**:
  May hallucinate facts; trained on English-heavy corpus (bias risk).

## Training Data
Subset of The Pile + open-license web data, filtered for quality.

## Evaluation
Perplexity 6.2 on WikiText-103; 29.5 ROUGE-L on XSum summarization.

## Ethical Considerations
Potential misuse for generating disallowed content; outputs should be moderated.

## Citation
If you use this model, please cite:
```
@software{ TinyLlama-1.1B,
  title={{ "TinyLlama-1.1B" }},
  author={{ "TinyLlama project" }},
  year=2025
}
```
```

---

## Custom Templates

Pass `--template custom_card.md.jinja` (or set `template:` in the workflow inputs) to swap in your own Jinja2 template. All metadata keys shown in the default template remain available.

---

© 2025  – MIT License
