ADMIN_TYPE = "Admin"
MANAGER_TYPE = "Manager"
DEVELOPER_TYPE = "Developer"
TESTER_TYPE = "Tester"
CADMIN_TYPE = "CAdmin"
CUSER_TYPE = "CUser"


class _User:
    def __init__(self):
        self.read_scopes = [
            ]
        self.write_scopes = [
            ]
        self.delete_scopes = [
            ]
        
    def has_access(self, to_endpoint, _type):
        scopes = getattr(self, f"{_type}_scopes")
        
        return to_endpoint in scopes
    def __str__(self) -> str:
        return str(self.__repr__())


class CUser(_User):
    def __init__(self, *args, **kwargs):
        super(CUser, self).__init__(*args, **kwargs)
        self.read_scopes = [
                "contacts",
            ]
        self.write_scopes = [
                "contacts",
            ]
        self.delete_scopes = [
                "contacts",
            ]
    
    def __repr__(self):
        return CUSER_TYPE


class CAdmin(CUser):
    def __init__(self, *args, **kwargs):
        super(CAdmin, self).__init__(*args, **kwargs)
        self.read_scopes.extend([
            CADMIN_TYPE,
            CUSER_TYPE
        ])
        self.write_scopes.extend([
            CADMIN_TYPE,
            CUSER_TYPE
        ])
        self.delete_scopes.extend([
            CADMIN_TYPE,
            CUSER_TYPE
        ])
    def __repr__(self):
        return CADMIN_TYPE
    

class Tester(_User):
    def __init__(self, *args, **kwargs):
        super(Tester, self).__init__(*args, **kwargs)
        self.read_scopes.extend([
            TESTER_TYPE
        ])
        self.write_scopes.extend([
            TESTER_TYPE
        ])
        self.delete_scopes.extend([
            TESTER_TYPE
        ])
    def __repr__(self):
        return TESTER_TYPE
    

class Developer(Tester):
    def __repr__(self):
        return DEVELOPER_TYPE
    

class Manager(CAdmin, Developer):
    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.read_scopes.extend([
            DEVELOPER_TYPE
        ])
        self.write_scopes.extend([
            DEVELOPER_TYPE
        ])
        self.delete_scopes.extend([
            DEVELOPER_TYPE
        ])
    def __repr__(self):
        return MANAGER_TYPE
    
class Admin(Manager):
    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.read_scopes.extend([
            MANAGER_TYPE
        ])
        self.write_scopes.extend([
            MANAGER_TYPE
        ])
        self.delete_scopes.extend([
            MANAGER_TYPE
        ])
    def __repr__(self):
        return ADMIN_TYPE





ACCOUNT_TYPES = {
    ADMIN_TYPE: Admin,
    CADMIN_TYPE: CAdmin,
    CUSER_TYPE: CUser,
    MANAGER_TYPE: Manager,
    DEVELOPER_TYPE: Developer,
}
