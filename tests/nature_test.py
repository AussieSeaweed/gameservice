import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        from gameservice.game.player import Nature

        nature = Nature(None)

        self.assertEqual(nature.actions, None)


if __name__ == '__main__':
    unittest.main()
