from pathlib import Path

import pytest

from tuned_lens.__main__ import main


def test_eval_subcommand(
    text_dataset_path: Path, gpt2_tiny_random_model_local_path: Path, tmp_path: Path
):
    # Note we do not specify a lens here, so we are using the logit lens
    args = (
        f"--log_level DEBUG eval --data.name {text_dataset_path}"
        f" --model.name {gpt2_tiny_random_model_local_path}"
        " --record_logit_stats"
        " --tokens 4000 --max_length 128"
        " --logit"
        f" --output {tmp_path}"
    )
    args = args.split()
    main(args)


def test_eval_subcommand_fails_when_not_enough_data_given(
    text_dataset_path: Path, gpt2_tiny_random_model_local_path: Path, tmp_path: Path
):
    args = (
        f"--log_level DEBUG eval --data.name {text_dataset_path}"
        f" --model.name {gpt2_tiny_random_model_local_path}"
        " --record_logit_stats"
        " --tokens 100000 --max_length 128"
        " --logit"
        f" --output {tmp_path}"
    )
    args = args.split()
    with pytest.raises(ValueError, match="Requested to evaluate on"):
        main(args)


def test_train_subcommand(
    text_dataset_path: Path, gpt2_tiny_random_model_local_path: Path, tmp_path: Path
):
    args = (
        f"--log_level DEBUG train --data.name {text_dataset_path}"
        f" --model.name {gpt2_tiny_random_model_local_path}"
        " --max_length 128"
        " --tokens_per_step 256"
        " --num_steps 4"
        " --checkpoint_freq 2"
        f" --output {tmp_path}"
    )
    args = args.split()
    main(args)
    assert Path(tmp_path, "checkpoints/snapshot_2.pth").exists()
    assert Path(tmp_path, "config.json").exists()
    assert Path(tmp_path, "params.pt").exists()


def test_train_subcommand_fails_when_not_enough_data_given(
    text_dataset_path: Path, gpt2_tiny_random_model_local_path: Path, tmp_path: Path
):
    args = (
        f"--log_level DEBUG train --data.name {text_dataset_path}"
        f" --model.name {gpt2_tiny_random_model_local_path}"
        " --max_length 128"
        " --tokens_per_step 256"
        " --num_steps 100000"
        " --checkpoint_freq 2"
        f" --output {tmp_path}"
    )
    args = args.split()
    with pytest.raises(ValueError, match="Can only take"):
        main(args)
