import copy
import unittest
from validate_plan import validate


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = {'assignments': [{
            'phone': '79990000001', 'member_id': '101', 'abonent_id': '201',
            'profile_id': '301', 'label': 'СЕВЕР / МП УД / Моб / Иванова А.Б.',
            'schema_name': 'Индивидуальная схема Ивановой',
            'route': [
                {'target': 'MEMBER', 'target_id': '101', 'timeout_seconds': 20},
                {'target': 'MEMBER', 'target_id': '102', 'timeout_seconds': 20},
                {'target': 'ACD', 'target_id': '501'},
            ],
        }]}

    def test_valid(self):
        self.assertEqual(validate(self.plan), [])

    def test_duplicate_assignments_rejected(self):
        self.plan['assignments'].append(copy.deepcopy(self.plan['assignments'][0]))
        self.assertTrue(any('duplicate' in e for e in validate(self.plan)))

    def test_label_limit(self):
        self.plan['assignments'][0]['label'] = 'Я' * 41
        self.assertTrue(any('40-symbol' in e for e in validate(self.plan)))

    def test_wrong_member_and_timeout(self):
        self.plan['assignments'][0]['route'][0].update(target_id='999', timeout_seconds=True)
        self.assertEqual(len(validate(self.plan)), 2)

    def test_malformed_input(self):
        for value in (None, {}, {'assignments': [None]}, {'assignments': []}):
            self.assertTrue(validate(value))

    def test_non_mobile_rejected(self):
        self.plan['assignments'][0]['phone'] = '74950000000'
        self.assertTrue(any('mobile' in e for e in validate(self.plan)))


if __name__ == '__main__':
    unittest.main()
