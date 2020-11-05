
def manhattan_temporal_delta_quant(a, b):
    """
    Return the manhattan distance from one temporal location to another

    Parameters
    ----------
    :param a: temporal location a
    :param b: temporal location b

    Returns
    -------
    :return: Scalar value denoting the manhattan distance between a and b
    """
    return abs(a - b)

def max_class_score(items_scores, return_total=False):
    best = (None, -1)
    total = float(0)
    for item_score in items_scores.items():
        total += item_score[1]
        if best[1] < item_score[1]:
            best = item_score
    return best if not return_total else best, total
