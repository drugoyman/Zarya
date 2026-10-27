"""Pure offline plan validation. No APIs, credentials, files written or mutations."""
import argparse
import json
import re
from pathlib import Path


def validate(plan):
    errors = []
    if not isinstance(plan, dict):
        return ['Plan must be an object']
    rows = plan.get('assignments')
    if not isinstance(rows, list) or not rows:
        return ['assignments must be a nonempty list']
    seen = {k: set() for k in ('phone', 'member_id', 'abonent_id', 'profile_id', 'schema_name')}
    for i, row in enumerate(rows, 1):
        prefix = f'assignment {i}: '
        if not isinstance(row, dict):
            errors.append(prefix + 'must be an object')
            continue
        phone = str(row.get('phone', ''))
        if not re.fullmatch(r'79\d{9}', phone):
            errors.append(prefix + 'phone must be normalized Russian mobile 79XXXXXXXXX')
        for key in ('member_id', 'abonent_id', 'profile_id'):
            if not re.fullmatch(r'[1-9]\d*', str(row.get(key, ''))):
                errors.append(prefix + key + ' must be a positive numeric ID')
        for key in ('label', 'schema_name'):
            value = row.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(prefix + key + ' must be nonempty text')
            elif key == 'label' and len(value) > 40:
                errors.append(prefix + 'label exceeds Mango 40-symbol limit')
        for key, values in seen.items():
            value = str(row.get(key, ''))
            if value in values:
                errors.append(prefix + 'duplicate ' + key)
            values.add(value)
        steps = row.get('route')
        if not isinstance(steps, list) or not steps:
            errors.append(prefix + 'route must be a nonempty list')
            continue
        for j, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                errors.append(prefix + f'route step {j} must be an object')
                continue
            if step.get('target') not in ('MEMBER', 'ACD'):
                errors.append(prefix + f'route step {j} must target MEMBER or ACD')
            if not re.fullmatch(r'[1-9]\d*', str(step.get('target_id', ''))):
                errors.append(prefix + f'route step {j} target_id must be positive numeric ID')
            timeout = step.get('timeout_seconds')
            if step.get('target') == 'MEMBER' and (
                isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0
            ):
                errors.append(prefix + f'route step {j} needs positive integer timeout_seconds')
        first = steps[0]
        if isinstance(first, dict) and (
            first.get('target') != 'MEMBER'
            or str(first.get('target_id')) != str(row.get('member_id'))
        ):
            errors.append(prefix + 'first step must target this assignment member')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    errors = validate(json.loads(args.plan.read_text(encoding='utf-8-sig')))
    print(json.dumps({'valid': not errors, 'errors': errors}, ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
