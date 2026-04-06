"""
Example usage of the Smart Library Request Workflow system
This script demonstrates how to use the core functionality
"""

from app import create_app
from services import RequestService, UserService, AnalyticsService, NotificationService
from models import UserRole


def main():
    """Example workflow demonstration"""
    
    print("=" * 80)
    print("Smart Library Request Workflow - Example Usage")
    print("=" * 80)
    
    # Initialize app and database
    app = create_app('development')
    db = app.SessionLocal()
    
    try:
        # ====================================================================
        # Step 1: Create Users
        # ====================================================================
        print("\n[1] Creating Users...")
        user_service = UserService(db)
        
        # Check or create requester
        requester = user_service.get_user_by_email('alice@library.com')
        if not requester:
            requester = user_service.create_user(
                username='alice_johnson',
                email='alice@library.com',
                full_name='Alice Johnson',
                role=UserRole.REQUESTER,
                department='Research'
            )
        print(f"  ✓ Requester: {requester.full_name}")
        
        # Check or create approver
        approver = user_service.get_user_by_email('bob@library.com')
        if not approver:
            approver = user_service.create_user(
                username='bob_smith',
                email='bob@library.com',
                full_name='Bob Smith',
                role=UserRole.APPROVER,
                department='Administration'
            )
        print(f"  ✓ Approver: {approver.full_name}")
        
        # Check or create admin
        admin = user_service.get_user_by_email('admin@library.com')
        if not admin:
            admin = user_service.create_user(
                username='admin',
                email='admin@library.com',
                full_name='System Administrator',
                role=UserRole.ADMIN
            )
        print(f"  ✓ Admin: {admin.full_name}")
        
        # ====================================================================
        # Step 2: Create and Manage Requests
        # ====================================================================
        print("\n[2] Creating Requests...")
        req_service = RequestService(db)
        
        # Create request 1: Small budget request (no approval needed)
        request1 = req_service.create_request(
            requester_id=requester.id,
            title='Core Reference Materials',
            description='Essential dictionaries and encyclopedias',
            priority=4,
            budget=1500,
            department='Research'
        )
        print(f"  ✓ Created request: {request1.request_number}")
        
        # Add items to request 1
        item1 = req_service.add_item_to_request(
            request_id=request1.id,
            title='Oxford English Dictionary',
            item_type='book',
            author='Oxford University Press',
            isbn='978-0-19-861185-3',
            quantity=1,
            unit_cost=245
        )
        print(f"    ├─ Added item: {item1.title}")
        
        item2 = req_service.add_item_to_request(
            request_id=request1.id,
            title='Encyclopedia Britannica Online',
            item_type='database',
            quantity=1,
            unit_cost=1255
        )
        print(f"    └─ Added item: {item2.title}")
        
        # Create request 2: Large budget request (needs approval)
        request2 = req_service.create_request(
            requester_id=requester.id,
            title='Research Database Bundle',
            description='Complete research database subscriptions',
            priority=1,  # High priority
            budget=15000,
            department='Research'
        )
        print(f"  ✓ Created request: {request2.request_number}")
        
        # Add items to request 2
        for i, (title, cost) in enumerate([
            ('JSTOR Access', 4000),
            ('ProQuest Dissertations', 3500),
            ('EBSCOhost', 3000),
            ('Scopus', 2500),
            ('Web of Science', 2000)
        ], 1):
            req_service.add_item_to_request(
                request_id=request2.id,
                title=title,
                item_type='database',
                quantity=1,
                unit_cost=cost
            )
        print(f"    └─ Added 5 database items")
        
        # ====================================================================
        # Step 3: Submit Requests
        # ====================================================================
        print("\n[3] Submitting Requests...")
        
        req_service.submit_request(request1.id, requester.id)
        print(f"  ✓ Submitted request 1 - Status: {request1.status.value}")
        
        req_service.submit_request(request2.id, requester.id)
        print(f"  ✓ Submitted request 2 - Status: {request2.status.value}")
        
        # Refresh to see updated status
        db.refresh(request2)
        print(f"    (Request 2 requires approval: {request2.status.value})")
        
        # ====================================================================
        # Step 4: Approve Request 2
        # ====================================================================
        print("\n[4] Processing Approvals...")
        
        if request2.status.value == 'pending_approval':
            req_service.approve_request(
                request2.id,
                approver.id,
                comments='Excellent research support package. Approved.'
            )
            db.refresh(request2)
            print(f"  ✓ Approved request 2 - Status: {request2.status.value}")
        
        # ====================================================================
        # Step 5: Complete Request 1
        # ====================================================================
        print("\n[5] Completing Request...")
        
        req_service.complete_request(request1.id)
        db.refresh(request1)
        print(f"  ✓ Completed request 1 - Status: {request1.status.value}")
        
        # ====================================================================
        # Step 6: Get Analytics
        # ====================================================================
        print("\n[6] Analytics Summary...")
        analytics_service = AnalyticsService(db)
        summary = analytics_service.get_requests_summary()
        
        print(f"  Total Requests: {summary['total_requests']}")
        print(f"  Pending Approval: {summary['pending_approval']}")
        print(f"  Approved: {summary['approved']}")
        print(f"  Completed: {summary['completed']}")
        print(f"  Rejected: {summary['rejected']}")
        print(f"  Approval Rate: {summary['approval_rate']:.1f}%")
        print(f"  Total Items: {summary['total_items']}")
        print(f"  Average Request Value: ${summary['average_request_value']:.2f}")
        
        # ====================================================================
        # Step 7: Get Status Breakdown
        # ====================================================================
        print("\n[7] Status Breakdown...")
        breakdown = analytics_service.get_requests_by_status_count()
        for status, count in breakdown.items():
            print(f"  {status}: {count}")
        
        # ====================================================================
        # Step 8: Get User Requests
        # ====================================================================
        print("\n[8] User Requests...")
        user_requests = req_service.get_user_requests(requester.id)
        print(f"  Requests from {requester.full_name}: {len(user_requests)}")
        for req in user_requests:
            print(f"  ├─ {req.request_number}: {req.title} ({req.status.value})")
        
        # ====================================================================
        # Step 9: Notifications
        # ====================================================================
        print("\n[9] Notifications...")
        notif_service = NotificationService(enabled=True)
        
        # Simulate notification sending
        notif_service.send_request_submitted_notification(
            requester.email,
            request1.request_number,
            request1.title,
            request1.id
        )
        
        notif_service.send_request_approved_notification(
            requester.email,
            request2.request_number,
            request2.title,
            request2.id
        )
        
        pending = notif_service.get_pending_notifications()
        print(f"  Pending Notifications: {len(pending)}")
        print(f"  Flushing notifications (printing to console)...")
        count = notif_service.flush_notifications()
        print(f"  ✓ Sent {count} notifications")
        
        print("\n" + "=" * 80)
        print("Example workflow completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()


if __name__ == '__main__':
    main()
