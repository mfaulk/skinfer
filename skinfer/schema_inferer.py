from __future__ import absolute_import, print_function

import json
import gzip
from skinfer.schema_generator import JsonSchemaGenerator
from skinfer.schema_merger import merge_schema


def gzopen(filename):
    """Opens file for reading as text, optionally gzipped
    """
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')

    return open(filename, 'rt')


def load_samples_from_jsonlines(file_list):
    for filename in file_list:
        with gzopen(filename) as f:
            for line in f:
                yield json.loads(line)


def load_samples_from_json(file_list):
    for filename in file_list:
        with gzopen(filename) as f:
            yield json.load(f)


def generate_schema_for_sample(sample):
    """Returns a schema generated for the given sample.
    """
    return JsonSchemaGenerator(sample).generate()


def generate_and_merge_schemas(samples):
    """Iterates through the given samples, generating schemas
    and merging them, returning the resulting merged schema.

    """
    merged = generate_schema_for_sample(next(iter(samples)))

    for sample in samples:
        merged = merge_schema(merged, generate_schema_for_sample(sample))

    return merged
