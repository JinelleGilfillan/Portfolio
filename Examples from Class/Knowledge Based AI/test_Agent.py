from unittest import TestCase
from Agent import Agent
from PIL import Image


class TestAgent(TestCase):
    def setUp(self):
        self.agent = Agent()


class TestProblemSolving(TestAgent):
    def test_problem_solving(self):
        problem = Image.open('C:/Users/jinel/Desktop/KBAI/KBAI-package-python-master/'\
                'KBAI-package-python-master/Project-Code-Python/Problems/Basic Problems B/'\
                'Basic Problem B-01/Basic Problem B-01.PNG')
        test = self.agent.Solve(problem)
        self.assertEqual(test, 2)
        problem.close()

