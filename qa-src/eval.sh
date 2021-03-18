python run_qa.py \
  --model_name_or_path Wikidepia\/indobert-lite-squad \
  --validation_file val_tmp.csv \
  --do_eval \
  --per_device_train_batch_size 64 \
  --max_seq_length 25 \
  --doc_stride 16 \
  --output_dir tmp/debug_squad/ \