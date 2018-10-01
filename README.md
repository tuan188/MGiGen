# igen - Code Generation Tools for iOS

## Installation:

### Install using pip:

Open Terminal and run:

```
$ pip install igen
```

### Update:

```
$ pip uninstall igen
$ pip install igen --no-cache-dir
```

### Uninstall:

```
$ pip uninstall igen
```

## How to install pip:

pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4

In order to install Python 2, you need to install Homebrew, run the following command in Terminal:

```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then install Python 2:

```
$ brew install python@2
```

## 1. Create Template:

### 1.1. Base Template:

The Base Template contains the necessary files for a scene in the Clean Architecture pattern.

Open Terminal, navigate to the folder you want to save the files and run:

```
$ igen template -base <Scene_Name>
```

The first time you use the template command, you need to enter project information:

```
Enter project name: Your Project
Enter developer name: Your Name
Enter company name: Your Company
```

Later, if you want to update the information you can run the command:

```
$ igen header
```

For example:
```
$ igen template -base Login
```

Output:

```
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

### 1.2. List Template:

The List Template shows a list of items in the UITableView or UICollectionView.

Copy the model to the pasteboard (clipboard) then run the command:

```
$ igen template -list <Scene_Name> [--section] [--collection]
```

**Option**:

--section: Show a list of items with header sections.

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

then run the command:

```
$ igen template -list ProductList
```

Output:
```
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

### 1.3. Detail Template:

The Detail Template shows item details in the UITableView.

Copy the model to the pasteboard then run the command:

```
$ igen template -detail <Scene_Name> [--static]
```

**Option**:

--static: Display item detail in a static UITableViewController.

For example :

Copy the following text to the pasteboard:

```
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then run the command:

```
$ igen template -detail ProductDetail
```
 
Output:

```
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
 
Finish!
```

## 2. Create model from json:

Copy the json to the pasteboard then run the command:

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

then run the command:

```
$ igen json Notice
```

Output:

```
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

Copy the protocol to the pasteboard then run the command:

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

then run the command:

```
$ igen mock
```

Output:

```
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

Copy the view model to the pasteboard then run the command:

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

then run the command:

```
$ igen test
```

Output:

```
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

Copy the model to the pasteboard then run the command:

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

then run the command:

```
$ igen init
```

Output:

```
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
