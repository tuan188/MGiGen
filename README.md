# iOS Tools

## 1. Create template:

### 1.1. Base template:

```
$ python it.py template -base <Scene_Name>
```

For example:
```
$ python it.py template -base Login
 
        new file:   Login/LoginViewModel.swift
        new file:   Login/LoginNavigator.swift
        new file:   Login/LoginUseCase.swift
        new file:   Login/LoginViewController.swift
        new file:   Login/Test/LoginViewModelTests.swift
        new file:   Login/Test/LoginUseCaseMock.swift
        new file:   Login/Test/LoginNavigatorMock.swift
        new file:   Login/Test/LoginViewControllerTests.swift
 
Finish!
```

### 1.2. List template:

Copy model text to clipboard then using command:
```
$ python it.py template -list <Scene_Name> [--section]
```

*Option*:
--section: Display list item with header sections.


For example :

Copy json text to clipboard:
```
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then using command:
```
 $ python it.py template -list ProductList

        new file:   ProductList/ProductListViewModel.swift
        new file:   ProductList/ProductListNavigator.swift
        new file:   ProductList/ProductListUseCase.swift
        new file:   ProductList/ProductListViewController.swift
        new file:   ProductList/ProductCell.swift
        new file:   ProductList/Test/ProductListViewModelTests.swift
        new file:   ProductList/Test/ProductListUseCaseMock.swift
        new file:   ProductList/Test/ProductListNavigatorMock.swift
        new file:   ProductList/Test/ProductListViewControllerTests.swift
        new file:   ProductList/Test/ProductCellTests.swift
 
Finish!
```

### 1.3. Detail template:

Copy model text to clipboard then using command:
```
$ python it.py template -detail <Scene_Name> [--static]
```

*Option*:
--static: Display item detail in static UITableView.


For example :

Copy json text to clipboard:
```
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then using command:
```
 $ python it.py template -detail ProductDetail
 
        new file:   ProductDetail/ProductDetailViewModel.swift
        new file:   ProductDetail/ProductDetailNavigator.swift
        new file:   ProductDetail/ProductDetailUseCase.swift
        new file:   ProductDetail/ProductDetailViewController.swift
        new file:   ProductDetail/ProductNameCell.swift
        new file:   ProductDetail/ProductPriceCell.swift
        new file:   ProductDetail/Test/ProductDetailViewModelTests.swift
        new file:   ProductDetail/Test/ProductDetailUseCaseMock.swift
        new file:   ProductDetail/Test/ProductDetailNavigatorMock.swift
        new file:   ProductDetail/Test/ProductDetailViewControllerTests.swift
        new file:   ProductDetail/Test/ProductDetailCellsTests.swift
 
Finish!
```

## 2. Create model from json:

Copy json text to clipboard then using command:

```
$ python it.py json <Model_Name>
```

For example :

Copy json text to clipboard:

```
{
    "id": 989,
    "content": "Hello world!",
    "is_read": false,
    "created_at": "2018-06-29T17:15:36+09:00"
}
```

then using command:
```
$ python it.py json Notice
Text has been copied to clipboard.
```

Clipboard:

```
import ObjectMapper
import Then

struct Notice {
    var id: Int
    var content: String
    var isRead: Bool
    var createdAt: Date
}

extension Notice {
    init() {
        self.init(
            id: 0
            content: ""
            isRead: false
            createdAt: Date()
        )
    }
}

extension Notice: Then { }

extension Notice: Mappable {

    init?(map: Map) {
        self.init()
    }

    mutating func mapping(map: Map) {
        id <- map["id"]
        content <- map["content"]
        isRead <- map["is_read"]
        createdAt <- (map["created_at"], DateTransform())
    }
}
```

## 3. Create mock for protocol:

Copy protocol text to clipboard then using command:

```
$ python it.py mock
```

For example :

Copy protocol text to clipboard:

```
protocol ProductsNavigatorType {
    func toProducts()
    func toProductDetail(product: Product)
    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate>
}
```

then using command:
```
$ python it.py mock
Text has been copied to clipboard.
```

Clipboard:

```
final class ProductsNavigatorMock: ProductsNavigatorType {

    // MARK: - toProducts
    var toProducts_Called = false

    func toProducts() {
        toProducts_Called = true
    }

    // MARK: - toProductDetail
    var toProductDetail_Called = false

    func toProductDetail(product: Product) {
        toProductDetail_Called = true
    }

    // MARK: - toEditProduct
    var toEditProduct_Called = false
    var toEditProduct_ReturnValue: Driver<EditProductDelegate> = Driver.empty()

    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate> {
        toEditProduct_Called = true
        return toEditProduct_ReturnValue
    }

}
```

## 4. Create unit tests for view model:

Copy view model text to clipboard then using command:

```
$ python it.py test
```

For example :

Copy view model text to clipboard:

```
struct AppViewModel: ViewModelType {

    struct Input {
        let loadTrigger: Driver<Void>
    }

    struct Output {
        let toMain: Driver<Void>
    }
```

then using command:
```
$ python it.py test
Text has been copied to clipboard.
```

Clipboard:

```
final class AppViewModelTests: XCTestCase {

    private var viewModel: AppViewModel!
    private var navigator: AppNavigatorMock!
    private var useCase: AppUseCaseMock!
    private var disposeBag: DisposeBag!

    private var input: AppViewModel.Input!
    private var output: AppViewModel.Output!
    private let loadTrigger = PublishSubject<Void>()

    override func setUp() {
        super.setUp()
        navigator = AppNavigatorMock()
        useCase = AppUseCaseMock()
        viewModel = AppViewModel(navigator: navigator, useCase: useCase)
        disposeBag = DisposeBag()

        input = AppViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()
        )
        output = viewModel.transform(input)
        output.toMain.drive().disposed(by: disposeBag)
    }

    func test_loadTriggerInvoked_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

}
```

## 5. Create init method for model:

Copy model text to clipboard then using command:

```
$ python it.py init
```

For example :

Copy model text to clipboard:

```
struct Product {
    var id: Int
    var name: String
    var price: Double
}
```

then using command:
```
$ python it.py init
Text has been copied to clipboard.
```

Clipboard:

```
extension Product {
    init() {
        self.init(
            id: 0,
            name: "",
            price: 0.0
        )
    }
}
```
