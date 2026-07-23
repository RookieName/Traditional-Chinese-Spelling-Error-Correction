def char_level_eval(source, pred, gold):

    min_len = min(
        len(source),
        len(pred),
        len(gold)
    )

    tp = fp = fn = tn = 0

    for i in range(min_len):

        source_char = source[i]
        pred_char = pred[i]
        gold_char = gold[i]

        # 原始字元本來就是錯的
        if source_char != gold_char:

            # 修正成功
            if pred_char == gold_char:
                tp += 1

            # 沒有修正成功
            else:
                fn += 1

        # 原始字元本來就是正確的
        else:

            # 保持正確
            if pred_char == gold_char:
                tn += 1

            # 把正確字改錯
            else:
                fp += 1

    return tp, fp, fn, tn


def compute_metrics(tp, fp, fn, tn):

    accuracy = (tp + tn) / (tp + tn + fp + fn + 1e-9)

    precision = tp / (tp + fp + 1e-9)

    recall = tp / ( tp + fn + 1e-9)

    f1 = 2 * precision * recall / (precision + recall + 1e-9)

    return accuracy, precision, recall, f1

"""
def char_level_eval(pred, gold):

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


"""
