import json
import pickle
import os
from opencc import OpenCC
import jieba
from pycorrector import MacBertCorrector
from trie import Trie
import math
import glob
from sklearn.metrics import precision_score, recall_score, f1_score
from correct_sys import correct_sys
from resources import *


DATA_DIR = "sighan_raw/pair_data/traditional"



def char_level_eval(pred, gold):
    """
    return TP, FP, FN
    """

    min_len = min(len(pred), len(gold))

    tp = fp = fn = 0

    for i in range(min_len):
        if pred[i] == gold[i]:
            tp += 1
        else:
            fp += 1
            fn += 1

    # 長度補償
    if len(pred) > len(gold):
        fp += len(pred) - len(gold)
    elif len(gold) > len(pred):
        fn += len(gold) - len(pred)

    return tp, fp, fn


def compute_metrics(all_tp, all_fp, all_fn):

    accuracy = all_tp / (all_tp + all_fp + all_fn + 1e-9)
    precision = all_tp / (all_tp + all_fp + 1e-9)
    recall = all_tp / (all_tp + all_fn + 1e-9)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)

    return accuracy, precision, recall, f1


# ----------------------------
# MacBERT baseline
# ----------------------------
def run_macbert(text):
    return macbert.correct(text).get("target", text)


# ----------------------------
# Your system
# ----------------------------
def run_yours(text):
    return correct_sys(text)


# ----------------------------
# Evaluate dataset
# ----------------------------
def evaluate():

    mac_tp = mac_fp = mac_fn = 0
    sys_tp = sys_fp = sys_fn = 0

    error_files = glob.glob(os.path.join(DATA_DIR, "test13_error.txt"))

    for error_file in error_files:

        correct_file = error_file.replace("_error.txt", "_correct.txt")

        if not os.path.exists(correct_file):
            continue

        with open(error_file, "r", encoding="utf-8") as f:
            error_text = f.read().strip()

        with open(correct_file, "r", encoding="utf-8") as f:
            gold_text = f.read().strip()

        # -------------------------
        # MacBERT
        # -------------------------
        mac_pred = run_macbert(error_text)
        tp, fp, fn = char_level_eval(mac_pred, gold_text)
        mac_tp += tp
        mac_fp += fp
        mac_fn += fn

        # -------------------------
        # Your system
        # -------------------------
        sys_pred = run_yours(error_text)
        tp, fp, fn = char_level_eval(sys_pred, gold_text)
        sys_tp += tp
        sys_fp += fp
        sys_fn += fn

        print("=================================")
        print("Error:", error_text)
        print("Gold :", gold_text)
        print("Mac  :", mac_pred)
        print("Yours:", sys_pred)

    # -------------------------
    # Metrics
    # -------------------------
    mac_metrics = compute_metrics(mac_tp, mac_fp, mac_fn)
    sys_metrics = compute_metrics(sys_tp, sys_fp, sys_fn)

    print("\n========== FINAL RESULT ==========")

    print("\n🔵 MacBERT")
    print(f"Accuracy : {mac_metrics[0]:.4f}")
    print(f"Precision: {mac_metrics[1]:.4f}")
    print(f"Recall   : {mac_metrics[2]:.4f}")
    print(f"F1       : {mac_metrics[3]:.4f}")

    print("\n🟢 Your System")
    print(f"Accuracy : {sys_metrics[0]:.4f}")
    print(f"Precision: {sys_metrics[1]:.4f}")
    print(f"Recall   : {sys_metrics[2]:.4f}")
    print(f"F1       : {sys_metrics[3]:.4f}")


if __name__ == "__main__":
    evaluate()