# iOS Tools

## Generate files for Clean Architecture:

```
$ python ca.py <Model_Name>
```

For example :
```
$ python ca.py Login

    new file:   Login/LoginViewModel.swift
    new file:   Login/LoginNavigator.swift
    new file:   Login/LoginUseCaseType.swift
    new file:   Login/LoginUseCase.swift
    new file:   Login/LoginViewController.swift
    new file:   Login/Test/LoginViewModelTests.swift
    new file:   Login/Test/LoginUseCaseMock.swift
    new file:   Login/Test/LoginNavigatorMock.swift
    new file:   Login/Test/LoginViewControllerTests.swift
    
Finish!
```

## Create model & builder file:
Copy json text to clipboard then using command:
```
$ python js.py <Model_Name>
```

For example :

Copy json text to clipboard:
```
{
    "id": 11,
    "name": "\u4e95\u4e0a \u592a\u4e00",
    "email": "sayuri97@example.org",
    "first_login": 1,
    "force_reset_password": 1,
    "birthday": "1997-06-30",
    "created_dt": "2018-03-22T12:15:49+09:00",
    "updated_dt": "2018-03-22T12:15:49+09:00"
}
```

then using command:
```
$ python js.py User

User.swift has been created.
Text has been copied to clipboard.
```

User.swift:
```
import ObjectMapper
import Then

struct User {
    let id: Int
    let name: String
    let email: String
    let firstLogin: Int
    let forceResetPassword: Int
    let birthday: Date
    let createdDt: Date
    let updatedDt: Date
}

final class UserBuilder: Then {
    var id: Int = 0
    var name: String = ""
    var email: String = ""
    var firstLogin: Int = 0
    var forceResetPassword: Int = 0
    var birthday: Date = Date()
    var createdDt: Date = Date()
    var updatedDt: Date = Date()

    init() {

    }

    init(user: User) {
        id = user.id
        name = user.name
        email = user.email
        firstLogin = user.firstLogin
        forceResetPassword = user.forceResetPassword
        birthday = user.birthday
        createdDt = user.createdDt
        updatedDt = user.updatedDt
    }
}

extension UserBuilder: Mappable {
    convenience init?(map: Map) {
        self.init()
    }

    func mapping(map: Map) {
        id <- map["id"]
        name <- map["name"]
        email <- map["email"]
        firstLogin <- map["first_login"]
        forceResetPassword <- map["force_reset_password"]
        birthday <- (map["birthday"], DateTransform())
        createdDt <- (map["created_dt"], DateTransform())
        updatedDt <- (map["updated_dt"], DateTransform())
    }
}

extension User {
    init(builder: UserBuilder) {
        self.init(
            id: builder.id,
            name: builder.name,
            email: builder.email,
            firstLogin: builder.firstLogin,
            forceResetPassword: builder.forceResetPassword,
            birthday: builder.birthday,
            createdDt: builder.createdDt,
            updatedDt: builder.updatedDt
        )
    }

    init() {
        self.init(builder: UserBuilder())
    }
}
```

## Create input builder from view model:

Copy view model text to clipboard then using command:

```
$ python ib.py
```

For example :

Copy view model text to clipboard:
```
struct NotificationsViewModel: ViewModelType {
    struct Input {
        let trigger: Driver<Void>
        let reloadTrigger: Driver<Void>
        let loadmoreTrigger: Driver<Void>
        let selectionTrigger: Driver<IndexPath>
    }
```

then using command:
```
$ python ib.py
Text has been copied to clipboard.
```

Result
```
extension NotificationsViewModel {
    struct InputBuilder {
       var trigger: Driver<Void> = Driver.empty()
       var reloadTrigger: Driver<Void> = Driver.empty()
       var loadmoreTrigger: Driver<Void> = Driver.empty()
       var selectionTrigger: Driver<IndexPath> = Driver.empty()
    }
}

extension NotificationsViewModel.Input {
    init(builder: NotificationsViewModel.InputBuilder) {
        self.init(
            trigger: builder.trigger,
            reloadTrigger: builder.reloadTrigger,
            loadmoreTrigger: builder.loadmoreTrigger,
            selectionTrigger: builder.selectionTrigger
        )
    }
}
```

## Create unit tests from view model:

Copy view model text to clipboard then using command:

```
$ python ut.py
```

For example :

Copy view model text to clipboard:
```
struct NotificationsViewModel: ViewModelType {
    struct Input {
        let trigger: Driver<Void>
        let reloadTrigger: Driver<Void>
        let loadmoreTrigger: Driver<Void>
        let selectionTrigger: Driver<IndexPath>
    }
    
    struct Output {
        let error: Driver<Error>
        let loading: Driver<Bool>
        let refreshing: Driver<Bool>
        let loadingMore: Driver<Bool>
        let fetchItems: Driver<Void>
        let notifications: Driver<[NotificationInfo]>
        let selectedNotification: Driver<Void>
    }
```

then using command:
```
$ python ib.py
Text has been copied to clipboard.
```

Result
```
final class NotificationsViewModelTests: XCTestCase {

    var viewModel: NotificationsViewModel!
    var navigator: NotificationsNavigatorMock!
    var useCase: NotificationsUseCaseMock!
    var disposeBag: DisposeBag!

    var input: NotificationsViewModel.Input!
    var output: NotificationsViewModel.Output!
    var trigger = PublishSubject<Void>()
    var reloadTrigger = PublishSubject<Void>()
    var loadmoreTrigger = PublishSubject<Void>()
    var selectionTrigger = PublishSubject<IndexPath>()

    override func setUp() {
        super.setUp()
        navigator = NotificationsNavigatorMock()
        useCase = NotificationsUseCaseMock()
        viewModel = NotificationsViewModel(navigator: navigator, useCase: useCase)
        disposeBag = DisposeBag()

        input = NotificationsViewModel.Input(
            trigger: trigger.asDriverOnErrorJustComplete(),
            reloadTrigger: reloadTrigger.asDriverOnErrorJustComplete(),
            loadmoreTrigger: loadmoreTrigger.asDriverOnErrorJustComplete(),
            selectionTrigger: selectionTrigger.asDriverOnErrorJustComplete()
        )
        output = viewModel.transform(input)
        output.error.drive().disposed(by: disposeBag)
        output.loading.drive().disposed(by: disposeBag)
        output.refreshing.drive().disposed(by: disposeBag)
        output.loadingMore.drive().disposed(by: disposeBag)
        output.fetchItems.drive().disposed(by: disposeBag)
        output.selectedNotification.drive().disposed(by: disposeBag)
    }

    func test_triggerInvoked_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

    func test_reloadTriggerInvoked_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

    func test_loadmoreTriggerInvoked_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

    func test_selectionTriggerInvoked_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

}

```

## Create mock class from protocol:

Copy protocol text to clipboard then using command:

```
$ python mock.py
```

For example :

Copy protocol text to clipboard:
```
protocol NotificationsUseCaseType {
    func getNotifications() -> Observable<PagingInfo<NotificationInfo>>
    func loadMoreNotifications(page: Int) -> Observable<PagingInfo<NotificationInfo>>
    func updateReadNotification(id: Int) -> Observable<Void>
}
```

then using command:
```
$ python mock.py
Text has been copied to clipboard.
```

Result
```
final class NotificationsUseCaseMock: NotificationsUseCaseType {

// MARK: - getNotifications

    var getNotifications_Called = false
    var getNotifications_ReturnValue: Observable<PagingInfo<NotificationInfo>> = Observable.empty()

    func getNotifications() -> Observable<PagingInfo<NotificationInfo>> {
        getNotifications_Called = true
        return getNotifications_ReturnValue
    }

// MARK: - loadMoreNotifications

    var loadMoreNotifications_Called = false
    var loadMoreNotifications_ReturnValue: Observable<PagingInfo<NotificationInfo>> = Observable.empty()

    func loadMoreNotifications(page: Int) -> Observable<PagingInfo<NotificationInfo>> {
        loadMoreNotifications_Called = true
        return loadMoreNotifications_ReturnValue
    }

// MARK: - updateReadNotification

    var updateReadNotification_Called = false
    var updateReadNotification_ReturnValue: Observable<Void> = Observable.empty()

    func updateReadNotification(id: Int) -> Observable<Void> {
        updateReadNotification_Called = true
        return updateReadNotification_ReturnValue
    }

}
```
