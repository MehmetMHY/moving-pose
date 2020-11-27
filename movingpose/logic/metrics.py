
def max_class_score(class_scores, return_total=False):
    """
    Get the class with the highest score, score (and score total) from a list of classes with scores

    Parameters
    ----------
    :param class_scores: list of classes with scores attached
        Format: [(class, score), ... (all items)]
    :param return_total: boolean denoting whether or not the total score should be returned

    Return
    ------
    :return: class with the highest score, score (and score total)
        Format: [[max_class, score], total]
    """
    best = (None, -1)
    total = float(0)
    for item_score in class_scores.items():
        total += item_score[1]
        if best[1] < item_score[1]:
            best = item_score
    return best if not return_total else best, total
