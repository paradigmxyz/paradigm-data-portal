import pdp


def test_get_global_manifest():
    global_manifest = pdp.get_global_manifest(source='remote')


def test_get_dataset_manifests():
    global_manifest = pdp.get_global_manifest(source='remote')
    for dataset_name in global_manifest['datasets'].keys():
        dataset_manifest = pdp.get_dataset_manifest(
            dataset_name, source='remote'
        )

