# Source Brief: Support Operations Incident Review

## Incident Summary

On Tuesday, a routing rules deployment sent high-priority enterprise tickets into the standard queue for 4 hours.

## Impact

- 187 tickets were delayed
- 23 enterprise customers experienced first-response SLA misses
- average first response time increased from 38 minutes to 2.6 hours
- customer sentiment dropped sharply in two strategic accounts

## Root Causes

- a config change was approved without a staged validation step
- alerting covered queue depth but not priority-routing mismatches
- the on-call runbook assumed queue overflow, not misclassification

## Recovery

- the routing change was rolled back within 25 minutes of detection
- a manual triage swarm cleared the backlog by end of day
- account teams sent follow-up notes to affected enterprise customers

## Prevention Ideas

1. add routing-diff validation before deploy
2. alert on queue priority mismatches
3. maintain an exec-ready incident summary template
