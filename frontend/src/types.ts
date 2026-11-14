export type PolicyId = 'P0' | 'P1' | 'A2' | 'P3';

export type VehicleState =
  | 'PARTIALLY_DISMANTLED'
  | 'REPAIR_MECHANICALLY_COMPLETE'
  | 'FINAL_VERIFICATION_IN_PROGRESS'
  | 'SAFE_TO_MOVE'
  | 'IN_CLEARANCE_TRANSIT'
  | 'IN_CUSTOMER_PICKUP_STAGING'
  | 'SAFE_TO_RELOCATE'
  | 'IN_RELOCATION_TRANSIT'
  | 'IN_HOLDING';

export type BayState = 'OCCUPIED' | 'CLEARANCE_PENDING' | 'AVAILABLE_FOR_ALLOCATION';

export type SolverStatus = 'OPTIMAL' | 'FEASIBLE' | 'INFEASIBLE' | 'UNKNOWN' | 'MODEL_INVALID';

export type ApprovalStatus = 'PENDING_APPROVAL' | 'APPROVED' | 'REJECTED' | 'STALE_SNAPSHOT';

export interface PartSource {
  source_id: string;
  name: string;
  usable_time_ticks: number;
  cost: number;
  atp: number;
  fitment_verified: boolean;
  quote_valid: boolean;
  source_version: number;
}

export interface RepairOrder {
  ro_id: string;
  customer_name: string;
  vehicle_model: string;
  is_commercial_fleet: boolean;
  promise_ticks: number;
  priority_weight: number;
  service_duration_ticks: number;
  required_bay: string;
  requires_alignment_hoist: boolean;
  current_vehicle_state: VehicleState;
  technician_signoff_recorded: boolean;
}

export interface ScheduledInterval {
  entity_type: string;
  entity_id: string;
  operation: string;
  start_tick: number;
  end_tick: number;
  start_clock: string;
  end_clock: string;
}

export interface RejectedOption {
  candidate_id: string;
  reason_code: string;
  description: string;
}

export interface Proposal {
  proposal_id: string;
  run_id: string;
  scenario_id: string;
  policy_id: PolicyId;
  input_snapshot_version: number;
  selected_source_id: string | null;
  selected_source_name: string | null;
  selected_movement: 'HOLD_ON_BAY' | 'RELOCATE_TO_H2';
  b4_release_tick: number;
  b4_release_clock: string;
  ro1051_finish_tick: number;
  ro1051_finish_clock: string;
  ro1042_finish_tick: number;
  ro1042_finish_clock: string;
  weighted_lateness_ticks: number;
  ro1042_lateness_ticks: number;
  ro1051_lateness_ticks: number;
  downstream_delay_minutes: number;
  parts_freight_cost: number;
  solver_status: SolverStatus;
  pass1_status?: SolverStatus | null;
  pass2_status?: SolverStatus | null;
  best_bound: number | null;
  solve_time_ms: number;
  feasibility_explanations: string[];
  rejected_options: RejectedOption[];
  scheduled_intervals: ScheduledInterval[];
  approval_status: ApprovalStatus;
}

export interface PolicyComparisonResult {
  scenario_id: string;
  snapshot_version: number;
  baseline_a2: Proposal;
  joint_p3: Proposal;
  weighted_lateness_reduction_pct: number;
  downstream_lateness_savings_minutes: number;
  freight_cost_delta: number;
  summary_verdict: string;
}

export interface ScenarioSnapshot {
  scenario_id: string;
  scenario_name: string;
  description: string;
  snapshot_version: number;
  current_tick: number;
  current_clock: string;
  ro1042: RepairOrder;
  ro1051: RepairOrder;
  sources: PartSource[];
  bay_b4_state: BayState;
  h2_capacity: number;
  h2_available_stalls: number;
  relocation_duration_ticks: number;
  clearance_duration_ticks: number;
  technician_k1_available: boolean;
}

export interface AuditEvent {
  event_id: string;
  timestamp: string;
  event_type: string;
  description: string;
  version_before: number;
  version_after: number;
  details: Record<string, any>;
}

export interface SolveResponse {
  comparison?: PolicyComparisonResult | null;
  active_proposal: Proposal;
  snapshot: ScenarioSnapshot;
}

export interface CompetingReservationResponse {
  status: string;
  affected_source: string;
  new_atp: number;
  new_snapshot_version: number;
  snapshot: ScenarioSnapshot;
}

export interface ApprovalResponse {
  success: boolean;
  status: string;
  message: string;
  proposal?: Proposal;
  old_proposal?: Proposal;
  new_proposal?: Proposal;
  new_comparison?: PolicyComparisonResult;
  requires_human_approval: boolean;
  current_snapshot?: ScenarioSnapshot;
}

export interface BenchmarkRecord {
  seed_id: string;
  a2_status: string;
  p3_status: string;
  a2_pass1_status?: string | null;
  a2_pass2_status?: string | null;
  p3_pass1_status?: string | null;
  p3_pass2_status?: string | null;
  a2_weighted_lateness: number;
  p3_weighted_lateness: number;
  a2_freight_cost: number;
  p3_freight_cost: number;
  relocation_selected: boolean;
  p3_outcome: string;
  delay_savings_min: number;
  p3_solve_time_ms: number;
  a2_solve_time_ms: number;
}

export interface BenchmarkResult {
  benchmark_id: string;
  total_seeds: number;
  valid_paired_seeds: number;
  master_seed: number;
  total_wall_clock_seconds: number;
  mean_p3_solve_time_ms: number;
  mean_a2_solve_time_ms: number;
  mean_a2_weighted_lateness: number;
  mean_p3_weighted_lateness: number;
  mean_downstream_delay_savings_min: number;
  mean_weighted_lateness_reduction_pct: number;
  p3_outperform_count: number;
  tie_count: number;
  p3_worsened_count: number;
  p3_win_or_tie_rate_pct: number;
  a2_status_distribution: Record<string, number>;
  p3_status_distribution: Record<string, number>;
  status_distribution?: Record<string, number>;
  artifact_path?: string;
  scope_notice?: string;
  records?: BenchmarkRecord[];
}
