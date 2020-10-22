try:
    one_entry = Entry.objects.get(blog=2000)
except Entry.DoesNotExist:
    # query did not match to any item.
    pass
except Entry.MultipleObjectsReturned:
    # query matched multiple items.
    pass
else:
    # query matched to just one item
    print(one_entry)

