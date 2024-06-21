# Run vLLM docker

Add HuggingFace token
```bash
docker run -d --name s2llm  --runtime nvidia --gpus all -v ~/.cache/huggingface:/root/.cache/huggingface -p 8000:8000 --env "HUGGING_FACE_HUB_TOKEN=REDACTED" vllm/vllm-openai:v0.4.3 --model="andy006/s2-oracle-trained" --tokenizer="andy006/s2-oracle-trained" --gpu-memory-utilization 0.9 --max-model-len 8192
```