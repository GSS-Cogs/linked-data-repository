from app.store.base import BaseStore
from app.store.drivers.stub.stub import StubStore

STORES = {"StubStore": StubStore}


def get_store(store_type_label: str) -> (BaseStore):
    """
    Gets a store from app/store/drivers based on the provided label
    """
    try:
        return STORES[store_type_label]()
    except KeyError as err:
        raise KeyError(
            f"No store of type {store_type_label} could be identified."
        ) from err


@given('I\'m using a store of type "{wanted_store}"')
def step_impl(context, wanted_store):
    context.store = get_store(wanted_store)
    context.store.setup()


@given('I get metadata for a resource identified by "{resource_id}"')
def step_impl(context, resource_id):
    context.metadata = context.store.get_resource(resource_id)


@then('"{count}" fields are returned')
def step_impl(context, count):
    got = len(context.metadata)
    expected = int(count)
    assert got == expected, f"Got {got} field, expected {expected}."


@then('there are "{count}" records with fields that match')
def step_impl(context, count):
    filter_kwargs = {}
    for row in context.table:
        filter_kwargs[row[0]] = row[1]

    matched_records = context.store.list_resources(**filter_kwargs)
    assert len(matched_records) == int(
        count
    ), f"Expected {int(count)} records, got {len(matched_records)}"


@given('I update a resource identified by "{resource_id}" with')
def step_impl(context, resource_id):
    for row in context.table:
        context.store.upsert_resource_field(resource_id, row[0], row[1])


@given('I create a new resource for the graph identifier "{graph_identifier}"')
def step_impl(context, graph_identifier):
    resource_id = context.store.create_resource(graph_identifier)
    context.metadata = context.store.get_resource(resource_id)
