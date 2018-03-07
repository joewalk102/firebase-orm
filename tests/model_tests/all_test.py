def test_necessary_collection(new_collection):
    model1 = new_collection()
    model2 = new_collection()
    for i in range(4):
        collection1 = model1(type_test='col1')
        collection1.save()
        collection2 = model2(type_test='col2')
        collection2.save()

    all_col_2 = model2.objects.all()
    types = [i.type_test for i in all_col_2]
    type_ = list(dict(zip(types, types)).values())

    assert type_ == ['col2']

