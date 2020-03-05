from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# 上传的文件能直接通过url打开，以及setting中设置
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt import views as simplejwt_views  # 引入simplejwt
from goods.views import GoodsListView, GoodsListViewSet, CategoryViewSet, ParentCategoryViewSet, BannerViewSet, IndexCategoryGoodsViewSet
from users.views import SendSmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, AddressViewSet
from trade.views import ShoppingCartViewSet, OrderInfoViewSet

# 创建一个路由器并注册我们的视图集
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, basename='goods')  # 配置goods的url
router.register(r'categories', CategoryViewSet, basename='categories')  # 配置分类的url
router.register(r'parent_categories', ParentCategoryViewSet, basename='parent_categories')  # 配置分类的url
router.register(r'code', SendSmsCodeViewSet, basename='code')  # 发送短信验证码
router.register(r'users', UserViewSet, basename='users')  # 用户注册
router.register(r'userfavs', UserFavViewSet, basename='userfavs')  # 用户收藏商品
router.register(r'livingmsgs', UserLeavingMessageViewSet, basename='livingmsgs')  # 用户留言
router.register(r'address', AddressViewSet, basename='address')  # 用户收货地址
router.register(r'shoppingcart', ShoppingCartViewSet, basename='shoppingcart')  # 购物车
router.register(r'orderinfo', OrderInfoViewSet, basename='orderinfo')  # 订单管理
router.register(r'banners', BannerViewSet, basename='banners')  # 首页轮播图
router.register(r'indexgoods', IndexCategoryGoodsViewSet, basename='indexgoods')  # 首页分类及商品

from trade.views import AliPayView
from user_operation.views import HotSearchView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # drf 认证url
    path('api-token-auth/', views.obtain_auth_token),  # drf token获取的url
    # path('api/token/', simplejwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # simplejwt认证接口
    path('login/', simplejwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录一般是login
    path('api/token/refresh/', simplejwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # simplejwt认证接口
    path('ckeditor/', include('ckeditor_uploader.urls')),  # 配置富文本编辑器url

    path('', include(router.urls)),  # API url现在由路由器自动确定。

    # DRF文档
    path('docs/', include_docs_urls(title='DRF文档')),

    # 支付宝通知接口
    path('alipay/return/', AliPayView.as_view(), name='alipay'),

    # 使用Django原生的TemplateView渲染index模板
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),

    # social_django认证登录
    path('', include('social_django.urls', namespace='social')),

    # 获取热搜
    path('hotsearchs/', HotSearchView.as_view(), name='hotsearchs')
]

# 上传的文件能直接通过url打开
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
