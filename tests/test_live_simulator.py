from creditlens.live.simulator import generate_snapshot


def test_generate_snapshot_is_reproducible_for_seed():
    first = generate_snapshot(seed=7)
    second = generate_snapshot(seed=7)

    assert first.observations == second.observations
    assert first.total_exposure == second.total_exposure
    assert first.average_modeled_pd == second.average_modeled_pd
    assert first.aggregate_expected_loss == second.aggregate_expected_loss
    assert first.aggregate_expected_revenue == second.aggregate_expected_revenue


def test_generate_snapshot_has_positive_portfolio_metrics():
    snapshot = generate_snapshot(seed=11)

    assert snapshot.observations > 0
    assert snapshot.total_exposure > 0
    assert 0 < snapshot.average_modeled_pd < 1
    assert snapshot.aggregate_expected_loss > 0
    assert snapshot.aggregate_expected_revenue > 0
    assert snapshot.pipeline_latency_ms > 0
