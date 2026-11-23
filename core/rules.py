"""Closed, pure validation predicates selected by GML registry declarations.
No eval, imports from GML, execution dispatch, or mutation of caller state.
"""
import math
from registry import RegistryError

class RuleViolation(ValueError): pass

def data_count(*, values, shape):
    if len(values)!=shape[0]*shape[1]: raise RuleViolation('data count does not match shape')

def finite_values(*, values):
    if any(type(x) not in (int,float) or not math.isfinite(x) for x in values):
        raise RuleViolation('data must be finite numbers')

def dtype_match(*, source_dtype, assembly_dtype, source_id):
    if source_dtype!=assembly_dtype:
        raise RuleViolation(f'dtype mismatch: assembly {assembly_dtype}, source {source_id} {source_dtype}')

def bounds_check(*, row, col, source_shape, target_shape):
    if row+source_shape[0]>target_shape[0] or col+source_shape[1]>target_shape[1]:
        raise RuleViolation('slice out of bounds')

def no_overlap(*, destination, occupied):
    if destination in occupied: raise RuleViolation(f'overlap at {destination}')

def complete_coverage(*, coverage_policy, occupied, total):
    if coverage_policy=='complete' and len(occupied)!=total:
        raise RuleViolation(f'incomplete coverage: {len(occupied)}/{total}')

PREDICATES={name:obj for name,obj in list(globals().items()) if name in {
    'data_count','finite_values','dtype_match','bounds_check','no_overlap','complete_coverage'}}

def check(registry, name, **context):
    rules=registry[2]
    predicate=rules.get(name)
    if predicate not in PREDICATES: raise RegistryError(f'unregistered or unsupported constraint: {name}')
    return PREDICATES[predicate](**context)
