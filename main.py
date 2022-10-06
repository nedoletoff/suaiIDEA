class IDEA(object):
    IDEAKEYSIZE = 16
    IDEABLOCKSIZE = 8
    IDEAROUNDS = 8
    IDEAKEYLEN = 6 * IDEAROUNDS + 4

    @staticmethod
    def pr():
        print(IDEA.IDEAKEYSIZE, " ",
              IDEA.IDEAROUNDS, " ",
              IDEA.IDEAKEYLEN, " ",
              IDEA.IDEAKEYLEN)


IDEA.pr()
l = list()
l.append("2")
print(l)
