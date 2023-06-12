from fuzzywuzzy import process

def basic_autocomplete(ctx, items):
    return list(
        filter(
            lambda x: x.lower().startswith(ctx.value.lower()),
            items
        )
    )

def fuzzy_autocomplete(ctx, items):
    return list(
        map(
            lambda x: x[0],
            process.extract(ctx.value.lower(), items)
        )
    )
