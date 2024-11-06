from base.tests.factories.ideal_candidate import IdealCandidateFactory


def run():
    for _ in range(5):
        ideal_candidates = IdealCandidateFactory()
        print(f'Created ideal_candidate: {ideal_candidates.name}')





