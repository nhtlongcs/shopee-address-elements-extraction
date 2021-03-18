python run_qa.py \
  --model_name_or_path Wikidepia\/indobert-lite-squad \
  --train_file train_0.csv \
  --validation_file val_0.csv \
  --do_train \
  --do_eval \
  --per_device_train_batch_size 1 \
  --learning_rate 3e-3 \
  --num_train_epochs 5 \
  --max_seq_length 25 \
  --doc_stride 16 \
  --output_dir tmp/debug_squad/ \
  --save_total_limit 3 \
  --eval_steps 500 \
  --no_cuda True \
  --save_steps 1000 \
  # --fp16 True \
  # --fp16_opt_level O2 \