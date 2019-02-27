# igen - Code Generation Tools for iOS

## Installation:
### Install using pip:
Open Terminal and run:

```
$ pip3 install igen
```

### Update:

```
$ pip3 install -U igen
```

or

```
$ pip3 uninstall igen
$ pip3 install igen --no-cache-dir
```

### Uninstall:

```
$ pip3 uninstall igen
```

## How to install pip3:
pip3 is already installed if you are using Python 3 (>=3.4)

In order to install Python 3, you need to install Homebrew, run the following command in Terminal:

```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then install Python 3:

```
$ brew install python
```

## 1. Create Template:
### 1.1. Base Template:
The Base Template contains necessary files for a screen using the [Clean Architecture](https://github.com/tuan188/MGCleanArchitecture) pattern.

Open Terminal, navigate to the folder you want to save the files and run:

```
$ igen template base <Scene_Name> [--window]
```

#### Options:

`--window`: use UIWindow instead of UINavigationController in the Navigator.

The first time you use the `template` command, you need to enter your project information:

```
Enter project name: Your Project
Enter developer name: Your Name
Enter company name: Your Company
```

Later, if you want to update the information you can run:

```
$ igen config project
```

#### Example:

```
$ igen template base Login
```

Output:

```
Successfully created files:
    Login/LoginViewModel.swift
    Login/LoginNavigator.swift
    Login/LoginUseCase.swift
    Login/LoginViewController.swift
    Login/LoginAssembler.swift
    Login/Test/LoginViewModelTests.swift
    Login/Test/LoginUseCaseMock.swift
    Login/Test/LoginNavigatorMock.swift
    Login/Test/LoginViewControllerTests.swift
```

### 1.2. Skeleton Template:
To create a Clean Architecture skeleton project, run:

```
$ igen template skeleton <Folder_Name>
```

#### Example:
Run the following command in Terminal:

```
$ igen template skeleton DemoApp
```

Output:

```
Successfully created files:
    DemoApp/Podfile
    DemoApp/Localizable.strings
    DemoApp/swiftlint.yml
    DemoApp/UnitTestViewController.swift
    DemoApp/AppDelegate.swift
    DemoApp/Medical-Bridging-Header.h
    DemoApp/Assembler/Assembler.swift
    DemoApp/Support/Utils.swift
    DemoApp/Extensions/UIViewController+.swift
    DemoApp/Extensions/UIViewController+Rx.swift
    DemoApp/Platform/Services/API/APIError.swift
    DemoApp/Platform/Services/API/APIService.swift
    DemoApp/Platform/Services/API/APIInput.swift
    DemoApp/Platform/Services/API/APIOutput.swift
    DemoApp/Platform/Services/API/APIUrls.swift
    DemoApp/Scenes/App/AppAssembler.swift
    DemoApp/Scenes/App/AppNavigator.swift
    DemoApp/Scenes/App/AppUseCase.swift
    DemoApp/Scenes/App/AppViewModel.swift
    DemoApp/Scenes/Storyboards/Storyboards.swift
```

### 1.3. List Template:
The List Template shows a list of objects in a UITableView or a UICollectionView.

Copy the model to the pasteboard (clipboard) then run:

```
$ igen template list <Scene_Name> [--section] [--collection] [--window]
```

#### Options:

`--section`: show the list with header sections.

`--collection`: use UICollectionView instead of UITableView.

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Copy the model:

```swift
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then run:

```
$ igen template list ProductList
```

Output:

```
Successfully created files:
    ProductList/ProductListViewModel.swift
    ProductList/ProductViewModel.swift
    ProductList/ProductListNavigator.swift
    ProductList/ProductListUseCase.swift
    ProductList/ProductListViewController.swift
    ProductList/ProductCell.swift
    ProductList/ProductListAssembler.swift
    ProductList/Test/ProductListViewModelTests.swift
    ProductList/Test/ProductListUseCaseMock.swift
    ProductList/Test/ProductListNavigatorMock.swift
    ProductList/Test/ProductListViewControllerTests.swift
    ProductList/Test/ProductCellTests.swift
```

### 1.4. Detail Template:
The Detail Template shows details of an object in a UITableView.

Copy the model then run:

```
$ igen template detail <Scene_Name> [--static] [--window]
```

#### Options:

`--static`: display details of the object in a static UITableViewController.

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Copy the model:

```swift
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then run:

```
$ igen template detail ProductDetail
```

Output:

```
Successfully created files:
    ProductDetail/ProductDetailViewModel.swift
    ProductDetail/ProductDetailNavigator.swift
    ProductDetail/ProductDetailUseCase.swift
    ProductDetail/ProductDetailViewController.swift
    ProductDetail/ProductIdCell.swift
    ProductDetail/ProductNameCell.swift
    ProductDetail/ProductPriceCell.swift
    ProductDetail/ProductDetailAssembler.swift
    ProductDetail/Test/ProductDetailViewModelTests.swift
    ProductDetail/Test/ProductDetailUseCaseMock.swift
    ProductDetail/Test/ProductDetailNavigatorMock.swift
    ProductDetail/Test/ProductDetailViewControllerTests.swift
    ProductDetail/Test/ProductDetailCellsTests.swift
```

### 1.5. Form Input Template:
To create a form input template for a model, copy the model then run:

```
$ igen template form <Scene_Name> [--submit SUBMIT] [--dynamic] [--window]
```

#### Options:

`--submit`: set the name of the submit action.

`--dynamic`: use the dynamic form instead of the static form.

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Copy the model:

```swift
struct Product {
    var id: Int
    var name: String
    var price: Double
}
```

then run:

```
$ igen template form CreateProduct --submit Create
```

Output:

```
Successfully created files:
    CreateProduct/CreateProductAssembler.swift
    CreateProduct/CreateProductNavigator.swift
    CreateProduct/CreateProductViewModel.swift
    CreateProduct/CreateProductUseCase.swift
    CreateProduct/CreateProductViewController.swift
    CreateProduct/Test/CreateProductUseCaseMock.swift
    CreateProduct/Test/CreateProductNavigatorMock.swift
    CreateProduct/Test/CreateProductViewModelTests.swift
    CreateProduct/Test/CreateProductViewControllerTests.swift
```

### 1.6. Setting Template:
Copy the enum then run:

```
$ igen template setting <Scene_Name> [--section] [--window]
```

#### Options:

`--section`: show the list with header sections.

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Copy the enum:

```swift
enum SettingMenu {
      case about
    case support
    case facebook
    case email
    case rating
}
```

then run:

```
$ igen template setting Setting
```

Output:

```
Successfully created files:
    Setting/SettingAssembler.swift
    Setting/SettingNavigator.swift
    Setting/SettingViewModel.swift
    Setting/SettingUseCase.swift
    Setting/SettingViewController.swift
    Setting/SettingMenuCell.swift
    Setting/Test/SettingUseCaseMock.swift
    Setting/Test/SettingNavigatorMock.swift
    Setting/Test/SettingViewModelTests.swift
    Setting/Test/SettingViewControllerTests.swift
    Setting/Test/SettingMenuCellTests.swift
```

## 2. Create a mock class for a protocol/function:
Copy the protocol/function then run:

```
$ igen mock [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:
Copy the protocol:

```swift
protocol ProductsNavigatorType {
    func toProducts()
    func toProductDetail(product: Product)
    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate>
}
```

then run:

```
$ igen mock
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

```swift
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

## 3. Create unit tests for a view model:
Copy the view model then run:

```
$ igen test [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:

Copy the model:

```swift
struct AppViewModel: ViewModelType {

    struct Input {
        let loadTrigger: Driver<Void>
    }

    struct Output {
        let toMain: Driver<Void>
    }
```

then run:

```
$ igen test
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

```swift
final class AppViewModelTests: XCTestCase {
    private var viewModel: AppViewModel!
    private var navigator: AppNavigatorMock!
    private var useCase: AppUseCaseMock!

    private var input: AppViewModel.Input!
    private var output: AppViewModel.Output!

    private var disposeBag: DisposeBag!

    private let loadTrigger = PublishSubject<Void>()

    override func setUp() {
        super.setUp()
        navigator = AppNavigatorMock()
        useCase = AppUseCaseMock()
        viewModel = AppViewModel(navigator: navigator, useCase: useCase)

        input = AppViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()
        )

        output = viewModel.transform(input)

        disposeBag = DisposeBag()

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

## 4. Create a initialize method for a class/struct:
Copy the class/struct then run the command:

```
$ igen init [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:

Copy the model:

```swift
struct Product {
    var id: Int
    var name: String
    var price: Double
}
```

then run:

```
$ igen init
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

```swift
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

## 5. Create models from JSON:
Copy the json then run the command:

```
$ igen json <Model_Name> [-p]
```

#### Options:

`—return-classes`: return classes instead of structs.

`-p`, `--print`: print the result.

#### Example:
Copy the json:

```json
{
    "id": 989,
    "content": "Hello world!",
    "is_read": false,
    "created_at": "2018-06-29T17:15:36+09:00"
}
```

then run:

```
$ igen json Notice
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

```swift
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

## 6. Configuration:
### 6.1. Configure the project information:
To update the project information, run:

```
$ igen config project
```

If you want to update the project name only, run:

```
$ igen config project.name <Project_Name>
```

Update the developer name:

```
$ igen config project.developer <Developer_Name>
```

Update the company name:

```
$ igen config project.company <Company_Name>
```

### 6.2. Configure the output path:
To configure the path for the output files, run:

```
$igen config output.path <Path>
```

#### Example:
Set the current working directory as the output path (relative path):

```
$igen config output.path .
```

Set the desktop as the output path:

```
$igen config output.path /Users/<Your_Name>/Desktop
```

You can use a special value `@here`  to set the current working directory as the output path (absolute path):

```
$igen config output.path @here
```

### 6.3. View the configuration:
To view the configuration, run:

```
$ igen config info
```

## 7. Other commands:
Run:

```
$ igen -h
```
