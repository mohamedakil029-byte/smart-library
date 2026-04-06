"""Workflow State Machine for Request Processing"""

from enum import Enum
from datetime import datetime
from typing import List, Optional, Dict, Any


class WorkflowTransition:
    """Represents a valid workflow transition"""
    
    def __init__(self, from_state: str, to_state: str, requires_approval: bool = False):
        self.from_state = from_state
        self.to_state = to_state
        self.requires_approval = requires_approval


class RequestWorkflow:
    """Smart Library Request Workflow Engine"""
    
    # Define valid state transitions
    VALID_TRANSITIONS = [
        WorkflowTransition('draft', 'submitted', requires_approval=False),
        WorkflowTransition('submitted', 'pending_approval', requires_approval=False),
        WorkflowTransition('submitted', 'in_progress', requires_approval=False),
        WorkflowTransition('pending_approval', 'approved', requires_approval=True),
        WorkflowTransition('pending_approval', 'rejected', requires_approval=True),
        WorkflowTransition('approved', 'in_progress', requires_approval=False),
        WorkflowTransition('in_progress', 'completed', requires_approval=False),
        WorkflowTransition('draft', 'cancelled', requires_approval=False),
        WorkflowTransition('submitted', 'cancelled', requires_approval=False),
        WorkflowTransition('pending_approval', 'cancelled', requires_approval=False),
        WorkflowTransition('rejected', 'draft', requires_approval=False),  # Allow resubmission
    ]
    
    def __init__(self):
        self.state_map = self._build_state_map()
    
    def _build_state_map(self) -> Dict[str, List[str]]:
        """Build map of valid next states for each state"""
        state_map = {}
        for transition in self.VALID_TRANSITIONS:
            if transition.from_state not in state_map:
                state_map[transition.from_state] = []
            state_map[transition.from_state].append(transition.to_state)
        return state_map
    
    def can_transition(self, current_state: str, target_state: str) -> bool:
        """Check if transition is valid"""
        if current_state not in self.state_map:
            return False
        return target_state in self.state_map[current_state]
    
    def get_valid_next_states(self, current_state: str) -> List[str]:
        """Get all valid next states from current state"""
        return self.state_map.get(current_state, [])
    
    def should_require_approval(self, from_state: str, to_state: str) -> bool:
        """Check if transition requires approval"""
        for transition in self.VALID_TRANSITIONS:
            if transition.from_state == from_state and transition.to_state == to_state:
                return transition.requires_approval
        return False
    
    def evaluate_request_for_approval(self, total_items: int, budget: int, 
                                     priority: int, threshold: int = 5) -> bool:
        """
        Determine if request needs approval based on criteria
        
        Args:
            total_items: Number of items in request
            budget: Total budget for request
            priority: Priority level (1=highest)
            threshold: Item count threshold for approval requirement
            
        Returns:
            True if approval is required
        """
        # Require approval if items exceed threshold
        if total_items >= threshold:
            return True
        
        # Require approval for high-priority or high-budget requests
        if priority <= 2 or budget > 10000:  # High priority or high budget
            return True
        
        return False
    
    def get_required_approvers(self, request: Any) -> List[str]:
        """
        Determine who needs to approve based on request details
        
        Args:
            request: Request object
            
        Returns:
            List of approver roles required
        """
        approvers = []
        
        # Budget-based approval
        if request.budget > 5000:
            approvers.append('library_director')
        if request.budget > 1000:
            approvers.append('department_head')
        
        # Default approver
        if 'department_head' not in approvers:
            approvers.append('head_librarian')
        
        return approvers


class WorkflowEngine:
    """Main workflow execution engine"""
    
    def __init__(self):
        self.workflow = RequestWorkflow()
        self.history = []
    
    def execute_transition(self, request_id: str, from_state: str, to_state: str, 
                          actor: str, metadata: Optional[Dict] = None) -> bool:
        """
        Execute a workflow transition
        
        Args:
            request_id: ID of the request
            from_state: Current state
            to_state: Target state
            actor: User performing transition
            metadata: Additional context data
            
        Returns:
            True if transition succeeded
        """
        if not self.workflow.can_transition(from_state, to_state):
            raise ValueError(f"Invalid transition from {from_state} to {to_state}")
        
        transition_event = {
            'request_id': request_id,
            'from_state': from_state,
            'to_state': to_state,
            'actor': actor,
            'timestamp': datetime.utcnow(),
            'metadata': metadata or {}
        }
        
        self.history.append(transition_event)
        return True
    
    def get_workflow_history(self, request_id: str) -> List[Dict]:
        """Get transition history for a request"""
        return [h for h in self.history if h['request_id'] == request_id]
