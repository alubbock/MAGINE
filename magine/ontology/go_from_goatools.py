from sys import modules

try:
    go = modules['go']
    termcounts = modules['termcounts']
    print('go and termcounts already exists')
except KeyError:
    print('Loading GO')
    from goatools import obo_parser
    from orangecontrib.bio.utils import serverfiles
    import os
    from goatools.associations import read_gaf
    from goatools.semantic import TermCounts

    os.environ[
        "PATH"] += os.pathsep + "C:\Users\James Pino\Miniconda2\envs\MAGINE\Library\\bin\graphviz"

    default_database_path = os.path.join(serverfiles.localpath(), "GO")

    short_path = os.path.join(default_database_path,
                              "gene_ontology_edit.obo.tar.gz",
                              "gene_ontology_edit.obo")

    if not os.path.exists(short_path):
        from orangecontrib.bio.go import Ontology

        print("Using ontology for first time")
        print("Downloading files via Orange.bio")
        ontology = Ontology()
        assert os.path.exists(short_path)

    go = obo_parser.GODag(short_path)
    associations = read_gaf(
            "http://geneontology.org/gene-associations/goa_human.gaf.gz")

    to_remove = set()
    for gene, terms in associations.items():
        terms_copy = terms.copy()
        for go_id in terms:
            if go_id not in go:
                terms_copy.remove(go_id)
        associations[gene] = terms_copy
    associations = {key: value for key, value in associations.items()
                    if value is not to_remove}
    termcounts = TermCounts(go, associations)
