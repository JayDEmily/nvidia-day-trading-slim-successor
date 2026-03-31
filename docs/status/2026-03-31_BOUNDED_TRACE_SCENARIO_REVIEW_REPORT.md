# Bounded Trace Scenario Review

Pack: `gate-132-bounded-trace-review-v1`

| Scenario | Desk window | Event window | Permission | Playbooks | Final risk | Deploy % | Human read |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| anchor_event_imminent | open_disorder | event_imminent_window | allow | none | derisk | 0.0000 | Should look cautious but not insane: no moon-buying, event-aware derisk, no crash. |
| clear_window_continuation | early_anchor | clear_window | allow | continuation_ladder | allow | 55.0000 | Should act like a normal supportive continuation: allow with one continuation playbook, not buy the moon. |
| lunch_flattened | lunch | clear_window | allow | none | allow | 0.0000 | Should look normal and quiet: allow posture, no active playbook, no explosion. |
| imminent_pin_derisk | open_disorder | event_imminent_window | allow | none | derisk | 0.0000 | Should derisk and stay small; still not a moon shot. |
| mild_down_block | open_disorder | event_imminent_window | derisk | none | block | 0.0000 | Should not explode; a hard block or equivalent stand-down is fine here. |

## Simplified narrative

- anchor_event_imminent: permission=allow; playbooks=['none']; final_risk=derisk; deploy=0.0000
- clear_window_continuation: permission=allow; playbooks=['continuation_ladder']; final_risk=allow; deploy=55.0000
- lunch_flattened: permission=allow; playbooks=['none']; final_risk=allow; deploy=0.0000
- imminent_pin_derisk: permission=allow; playbooks=['none']; final_risk=derisk; deploy=0.0000
- mild_down_block: permission=derisk; playbooks=['none']; final_risk=block; deploy=0.0000

