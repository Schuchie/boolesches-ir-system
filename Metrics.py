class Metrics:
    def __init__(self):
        pass

    def intersect(self, topN_results, ground_truth):
        inter = 0
        for res in topN_results:
            if res[0].upper() in ground_truth:
                inter += 1

        return inter

    def compute_precision_score(self, topN_results, ground_truth):
        inter = float(self.intersect(topN_results, ground_truth))
        p = inter / len(topN_results)
        return p

    def compute_recall_score(self, topN_results, ground_truth):
        inter = float(self.intersect(topN_results, ground_truth))
        r = inter / len(ground_truth)
        return r

    def compute_f1_score(self, topN_results, ground_truth):
        p = self.compute_precision_score(topN_results, ground_truth)
        r = self.compute_recall_score(topN_results, ground_truth)
        if p == 0. and r == 0.:
            f1 = 0.
        else:
            f1 = 2 * (p*r/(p+r))
        return f1
