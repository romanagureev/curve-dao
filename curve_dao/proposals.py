import datetime

import boa

TIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"


def get_datestring(ts):
    dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
    return dt.strftime(TIME_FORMAT)


def update_stableswap(
    pool,
    ramp_time_weeks,
    new_A,
    new_fee_bps,
    new_offpeg_fee_multiplier,
    proposal_time_weeks,
):
    SECONDS_PER_WEEK = 7 * 24 * 60 * 60
    FEE_SCALE = 10**6  # bps to int
    OFFPEG_FEE_MULTIPLIER_SCALE = 10**10  # bps to int

    ramp_time_seconds = int(ramp_time_weeks * SECONDS_PER_WEEK)
    proposal_time_seconds = int(proposal_time_weeks * SECONDS_PER_WEEK)
    scaled_fee = int(new_fee_bps * FEE_SCALE)
    scaled_offpeg_fee_multiplier = int(
        new_offpeg_fee_multiplier * OFFPEG_FEE_MULTIPLIER_SCALE
    )

    current_time = boa.env.evm.patch.timestamp
    future_A_time = current_time + ramp_time_seconds + proposal_time_seconds

    pool_address = pool.address.strip()
    actions = [
        (pool_address, "ramp_A", new_A, future_A_time),
        (pool_address, "set_new_fee", scaled_fee, scaled_offpeg_fee_multiplier),
    ]

    current_A = pool.A()
    current_fee_bps = pool.fee() / FEE_SCALE
    current_offpeg_multiplier = (
        pool.offpeg_fee_multiplier() / OFFPEG_FEE_MULTIPLIER_SCALE
    )
    ramp_start_time = future_A_time - ramp_time_seconds
    ramp_start_datestring = get_datestring(ramp_start_time)
    ramp_end_datestring = get_datestring(future_A_time)

    description = (
        f"Update StableswapNG parameters for pool {pool_address} with: "
        f"fee from {current_fee_bps} -> {new_fee_bps} bps, "
        f"offpeg multiplier from {current_offpeg_multiplier} -> {new_offpeg_fee_multiplier}, "
        f"amplification factor from {current_A} -> {new_A} ramped over {ramp_time_weeks} weeks "
        f"starting on {ramp_start_datestring} and ending on {ramp_end_datestring}."
    )

    return actions, description
