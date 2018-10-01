# iOS Tools

## Welcome:

igen is a Code Generator for iOS.

## Installation:

Using pip:

```
pip install igen
```

Update:

```
pip install -U igen
```

Uninstall:

```
pip uninstall igen
```

## How to install pip:

pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4

First you need to install Homebrew. To install Homebrew, open Terminal or your favorite OSX terminal emulator and run:

```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then install Python 2:

```
$ brew install python@2
```

## 1. Create template:

### 1.1. Base template:

```
$ igen template -base <Scene_Name>
```

For example:
```
igen t -base Login
 
        new file:   Login/LoginViewModel.swift
        new file:   Login/LoginNavigator.swift
        new file:   Login/LoginUseCase.swift
        new file:   Login/LoginViewController.swift
        new file:   Login/LoginAssembler.swift
        new file:   Login/Test/LoginViewModelTests.swift
        new file:   Login/Test/LoginUseCaseMock.swift
        new file:   Login/Test/LoginNavigatorMock.swift
        new file:   Login/Test/LoginViewControllerTests.swift
 
Finish!
```

### 1.2. List template:

Copy model to the pasteboard (clipboard) then use command:
```
$ igen template -list <Scene_Name> [--section] [--collection]
```

*Option*:
--section: Display a list of items with header sections.
--collection: Use UICollectionView instead of UITableView

For example :

Copy the following text to the pasteboard:
```
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then use command:
```
 $ igen template -list ProductList
 
        new file:   ProductList/ProductListViewModel.swift
        new file:   ProductList/ProductViewModel.swift
        new file:   ProductList/ProductListNavigator.swift
        new file:   ProductList/ProductListUseCase.swift
        new file:   ProductList/ProductListViewController.swift
        new file:   ProductList/ProductCell.swift
        new file:   ProductList/ProductListAssembler.swift
        new file:   ProductList/Test/ProductListViewModelTests.swift
        new file:   ProductList/Test/ProductListUseCaseMock.swift
        new file:   ProductList/Test/ProductListNavigatorMock.swift
        new file:   ProductList/Test/ProductListViewControllerTests.swift
        new file:   ProductList/Test/ProductCellTests.swift
 
Finish!
```

### 1.3. Detail template:

Copy model to the pasteboard then use command:
```
$ igen template -detail <Scene_Name> [--static]
```

*Option*:
--static: Display item detail in a static UITableView.

For example :

Copy the following text to the pasteboard:
```
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then use command:
```
 $ igen template -detail ProductDetail
 
        new file:   ProductDetail/ProductDetailViewModel.swift
        new file:   ProductDetail/ProductDetailNavigator.swift
        new file:   ProductDetail/ProductDetailUseCase.swift
        new file:   ProductDetail/ProductDetailViewController.swift
        new file:   ProductDetail/ProductIdCell.swift
        new file:   ProductDetail/ProductNameCell.swift
        new file:   ProductDetail/ProductPriceCell.swift
        new file:   ProductDetail/ProductDetailAssembler.swift
        new file:   ProductDetail/Test/ProductDetailViewModelTests.swift
        new file:   ProductDetail/Test/ProductDetailUseCaseMock.swift
        new file:   ProductDetail/Test/ProductDetailNavigatorMock.swift
        new file:   ProductDetail/Test/ProductDetailViewControllerTests.swift
        new file:   ProductDetail/Test/ProductDetailCellsTests.swift
 

```

## 2. Create model from json:

Copy json to the pasteboard then use command:

```
$ igen json <Model_Name>
```

For example :

Copy the following text to the pasteboard:

```
{
    "id": 989,
    "content": "Hello world!",
    "is_read": false,
    "created_at": "2018-06-29T17:15:36+09:00"
}
```

then use command:
```
$ igen json Notice
Text has been copied to clipboard.
```

Content in the pasteboard:

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
            id: 0,
            content: "",
            isRead: false,
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

Copy protocol to the pasteboard then use command:

```
$ igen mock
```

For example :

Copy the following text to the pasteboard:

```
protocol ProductsNavigatorType {
    func toProducts()
    func toProductDetail(product: Product)
    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate>
}
```

then using command:
```
$ igen mock
Text has been copied to clipboard.
```

Content in the pasteboard:

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

Copy view model to the pasteboard then use command:

```
$ igen test
```

For example :

Copy the following text to the pasteboard:

```
struct AppViewModel: ViewModelType {

    struct Input {
        let loadTrigger: Driver<Void>
    }

    struct Output {
        let toMain: Driver<Void>
    }
```

then use command:
```
$ igen test
Text has been copied to clipboard.
```

Content in the pasteboard:

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

    func test_loadTrigger_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

}
```

## 5. Create init method for model:

Copy model to the pasteboard then use command:

```
$ igen init
```

For example :

Copy the following text to the pasteboard:

```
struct Product {
    var id: Int
    var name: String
    var price: Double
}
```

then use command:
```
$ igen init
Text has been copied to clipboard.
```

Content in the pasteboard:

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
