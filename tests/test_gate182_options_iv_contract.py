from __future__ import annotations

from nvda_desk.schemas.cognition import OptionsFlowContextInput
from nvda_desk.services.options_flow_context import OptionsFlowContextService


def _payload(front_iv: float, next_iv: float, front_rv: float, next_rv: float) -> OptionsFlowContextInput:
    return OptionsFlowContextInput(
        spot_price=111.06,
        front_dte=4,
        next_dte=11,
        front_atm_iv=front_iv,
        next_atm_iv=next_iv,
        put_call_skew=0.055,
        gamma_pressure_score=0.72,
        call_put_imbalance=0.18,
        oi_concentration=0.61,
        atm_straddle_value=7.43,
        front_realised_vol=front_rv,
        next_realised_vol=next_rv,
    )


def test_gate182_percent_style_ingress_normalises_to_decimal_contract() -> None:
    payload = _payload(73.6, 71.4, 59.5, 58.0)

    assert payload.front_atm_iv == 0.736
    assert payload.next_atm_iv == 0.714
    assert payload.front_realised_vol == 0.595
    assert payload.next_realised_vol == 0.58


def test_gate182_mixed_percent_and_decimal_payloads_classify_identically() -> None:
    service = OptionsFlowContextService()

    decimal_result = service.evaluate(_payload(0.736, 0.714, 0.595, 0.58))
    percent_result = service.evaluate(_payload(73.6, 71.4, 59.5, 58.0))

    assert percent_result == decimal_result
    assert decimal_result.term_structure_state.value == "front_premium"
    assert decimal_result.iv_rv_front_state == "iv_rich"
    assert decimal_result.iv_rv_next_state == "iv_rich"
