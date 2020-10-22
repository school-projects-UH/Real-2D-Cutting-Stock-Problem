import coverage
COV = coverage.coverage(branch=True, include='src/*')
COV.start()

import unittest
suite = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2).run(suite)

COV.stop()
COV.report()
