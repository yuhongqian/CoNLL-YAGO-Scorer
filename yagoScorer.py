"""
Copyright 2020 HongChien Yu

This program is a scorer for the CoNLL-YAGO dataset
(https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/ambiverse-nlu/aida/.)

The scorer calculates micro average over all documents, where
    micro average = (total TP)/(total TP + total FP)
"""

from __future__ import division
from absl import flags, app

FLAGS = flags.FLAGS
flags.DEFINE_string("gold_std", None, "Path to AIDA-YAGO2-annotations.tsv. ")
flags.DEFINE_string("system_out", None, "Path to the system output file. ")
flags.DEFINE_string("report", None, "Path to the file for final report.")


class Scorer(object):

    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.goldStd = open(FLAGS.gold_std, "r")
        self.sysOut = open(FLAGS.system_out, "r")
        self.sysOut.readline() # skip the first "-DOCSTART-"
        self.report = None
        if (FLAGS.report != None):
            self.report = open(FLAGS.report, "a")
            self.report.write("The following outputs are wrong:\n")

    def calcOneDoc(self, goldDict):
        """
        Accumulate tf & fp for one document.
        :return: None.
        """
        sysLine = self.sysOut.readline()
        while sysLine:
            if sysLine.startswith("-DOCSTART-"):
                return  # stops at the beginning of next doc
            fields = sysLine.split()

            idx = fields[0]
            entity = fields[1]
            if idx in goldDict and entity == goldDict[idx]:
                self.tp += 1
            else:
                self.fp += 1
                self.report.write(sysLine)
            sysLine = self.sysOut.readline()

    def cleanUp(self):
        """
        Write summary to the report, then close all opened files.
        :return: The final score.
        """
        self.report.write("The number of true positives = %d\n" % self.tp)
        self.report.write("The number of false positives = %d\n" % self.fp)
        score = self.tp / (self.tp + self.fp)
        self.report.write("Micro average = tp / (tp + fp) = %f\n" % score)
        self.goldStd.close()
        self.sysOut.close()
        if self.report:
            self.report.close()
        return score

    def calculateScore(self):
        """
        :return: the final score of the system output.
        """
        goldDict = dict()
        goldLine = self.goldStd.readline()
        while goldLine:
            if goldLine.startswith("-DOCSTART-"):
                self.report.write(goldLine)
                goldDict = dict()   # token index -> linked Wikipedia string (1st column in the gold std)
            else:
                fields = goldLine.split()
                if len(fields) > 0:     # normal annotation line.
                    idx = fields[0]
                    entity = fields[1]
                    goldDict[idx] = entity
                else:   # end of current doc annotations.
                    self.calcOneDoc(goldDict)
            goldLine = self.goldStd.readline()
        score = self.cleanUp()
        return score


def main(_):
    scorer = Scorer()
    score = scorer.calculateScore()
    print("The final system score is %f" % score)


if __name__ == "__main__":
    flags.mark_flag_as_required("gold_std")
    flags.mark_flag_as_required("system_out")
    app.run(main)