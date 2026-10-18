import pytest

from day_11 import run_with_retry  


def test_timeout_then_success():
    calls = 0

    def flaky_operation():
        nonlocal calls
        calls += 1

        if calls < 3:
            raise TimeoutError("temporary timeout")

        return "success"

    result = run_with_retry(flaky_operation, max_attempts=3)

    assert result == "success"
    assert calls == 3


def test_value_error_is_not_retried():
    calls = 0

    def failing_operation():
        nonlocal calls
        calls += 1
        raise ValueError("invalid input")

    with pytest.raises(ValueError, match="invalid input"):
        run_with_retry(failing_operation, max_attempts=3)

    assert calls == 1


def test_connection_error_exhausts_attempts():
    calls = 0

    def failing_operation():
        nonlocal calls
        calls += 1
        raise ConnectionError("service unavailable")

    with pytest.raises(ConnectionError, match="service unavailable"):
        run_with_retry(failing_operation, max_attempts=3)

    assert calls == 3
def test_backoff_delays_are_calculated():
    calls = 0
    delays = []

    def operation():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise TimeoutError("temporary failure")
        return "success"

    def fake_sleep(seconds):
        delays.append(seconds)

    result = run_with_retry(
        operation,
        max_attempts=3,
        base_delay=0.25,
        max_delay=2.0,
        sleep_fn=fake_sleep,
        random_fn=lambda: 0.5,
    )

    assert result == "success"
    assert calls == 3
    assert delays == [0.125, 0.25]


def test_backoff_respects_max_delay():
    calls = 0
    delays = []

    def operation():
        nonlocal calls
        calls += 1
        raise TimeoutError("still failing")

    def fake_sleep(seconds):
        delays.append(seconds)

    with pytest.raises(TimeoutError, match="still failing"):
        run_with_retry(
            operation,
            max_attempts=5,
            base_delay=0.5,
            max_delay=1.0,
            sleep_fn=fake_sleep,
            random_fn=lambda: 0.5,
        )

    assert calls == 5
    assert delays == [0.25, 0.5, 0.5, 0.5]



@pytest.mark.parametrize("attempts", [0, -1, 2.5, True])
def test_invalid_max_attempts(attempts):
    with pytest.raises(ValueError):
        run_with_retry(lambda: "success", max_attempts=attempts)


@pytest.mark.parametrize(
    "delay",
    [-1.0, float("nan"), float("inf"), -float("inf")],
)
def test_invalid_base_delay(delay):
    with pytest.raises(ValueError):
        run_with_retry(lambda: "success", base_delay=delay)


@pytest.mark.parametrize(
    "delay",
    [-1.0, float("nan"), float("inf"), -float("inf")],
)
def test_invalid_max_delay(delay):
    with pytest.raises(ValueError):
        run_with_retry(lambda: "success", max_delay=delay)


def test_invalid_configuration_does_not_call_operation():
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        return "success"

    with pytest.raises(ValueError):
        run_with_retry(operation, max_attempts=0)

    assert calls == 0
def test_zero_max_delay_is_valid():
    calls = 0
    delays = []

    def operation():
        nonlocal calls
        calls += 1

        if calls == 1:
            raise TimeoutError("temporary failure")

        return "success"

    result = run_with_retry(
        operation,
        max_attempts=2,
        base_delay=0.25,
        max_delay=0.0,
        sleep_fn=delays.append,
        random_fn=lambda: 0.5,
    )

    assert result == "success"
    assert calls == 2
    assert delays == [0.0]