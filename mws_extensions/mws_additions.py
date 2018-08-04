from mws import mws
from mws.utils import next_token_action

from .utils import enumerate_dict, enumerate_list


class InboundShipments(mws.MWS):
    URI = "/FulfillmentInboundShipment/2010-10-01"
    VERSION = '2010-10-01'
    NAMESPACE = '{http://mws.amazonaws.com/FulfillmentInboundShipment/2010-10-01/}'
    NEXT_TOKEN_OPERATIONS = [
        'ListInboundShipments',
        'ListInboundShipmentItems',
    ]

    @next_token_action('ListInboundShipments')
    def list_inbound_shipments(self, shipment_status_list=None, shipment_id_list=None,
                               last_updated_after=None, last_updated_before=None, next_token=None):
        """
        Args:
            shipment_status_list (:obj:`list` of :obj:`ShipmentStatus`):
            shipment_id_list (:obj:`list` of :obj:`ShipmentStatus`):
            last_updated_after: A date used for selecting inbound shipments that were last updated after (or at) a
                specified time. The selection includes updates made by Amazon and by the seller.
            last_updated_before:  A date used for selecting inbound shipments that were last updated before (or at) a
                specified time. The selection includes updates made by Amazon and by the seller.
        Returns:
            :obj:`DictWrapper`
        """

        data = dict(Action='ListInboundShipments',
                    LastUpdatedAfter=last_updated_after,
                    LastUpdatedBefore=last_updated_before)
        data.update(enumerate_list('ShipmentStatusList.member.', shipment_status_list))
        data.update(enumerate_list('ShipmentIdList.member.', shipment_id_list))
        return self.make_request(data)

    @next_token_action('ListInboundShipmentItems')
    def list_inbound_shipment_items(self, shipment_id=None, last_updated_after=None,
                                    last_updated_before=None, next_token=None):
        """
        Returns a list of items contained in an inbound shipment that you specify with a ShipmentId.
        Alternatively, if you submit the LastUpdatedAfter and LastUpdatedBefore request parameters,
        the ListInboundShipmentItems operation returns inbound shipment items based on when the items
        were last updated. Note that if you specify the ShipmentId, then the LastUpdatedAfter and
        LastUpdatedBefore request parameters are ignored.
        Args:
            shipment_id:
            last_updated_after:
            last_updated_before:
        Returns:
            :obj:`DictWrapper`
        """

        data = dict(Action='ListInboundShipmentItems',
                    ShipmentId=shipment_id,
                    LastUpdatedAfter=last_updated_after,
                    LastUpdatedBefore=last_updated_before)
        return self.make_request(data)

    def inbound_guidance_for_sku(self, sku_inbound_guidance_list, marketplace_id):
        """
        The GetInboundGuidanceForSKU operation lets a seller know if Amazon recommends sending an item to a given
        marketplace. In some cases, Amazon provides guidance for why a given Seller SKU is not recommended for
        shipment to Amazon's fulfillment network.
        Args:
            sku_inbound_guidance_list:
            marketplace_id:
        Returns:
            :obj:`DictWrapper`
        """
        data = dict(Action='GetInboundGuidanceForSKU',
                    MarketplaceId=marketplace_id)

        data.update(enumerate_list('SellerSKUList.Id.', sku_inbound_guidance_list))
        return self.make_request(data)

    def inbound_guidance_for_asin(self, asin_inbound_guidance_list, marketplace_id):
        """
        The GetInboundGuidanceForASIN operation lets a seller know if Amazon recommends sending a product to a
        given marketplace. In some cases, Amazon provides guidance for why a given ASIN is not recommended for
        shipment to Amazon's fulfillment network.
        Args:
            asin_inbound_guidance_list:
            marketplace_id:
        Returns:
            :obj:`DictWrapper`
        """
        data = dict(Action='GetInboundGuidanceForASIN',
                    MarketplaceId=marketplace_id)

        data.update(enumerate_list('ASINList.Id.', asin_inbound_guidance_list))
        return self.make_request(data)

    def create_inbound_shipment_plan(self, ship_from_address, inbound_shipment_plan_request_items,
                                     ship_to_country_code=None, ship_to_country_ship_to_country_subdivision_code=None,
                                     label_prep_preference=None):
        """
        The CreateInboundShipmentPlan operation returns one or more inbound shipment plans, which provide the
        information you need to create one or more inbound shipments for a set of items that you specify.
        Multiple inbound shipment plans might be required so that items can be optimally placed in Amazon's
        fulfillment network—for example, positioning inventory closer to the customer. Alternatively, two inbound
        shipment plans might be created with the same Amazon fulfillment center destination if the two shipment plans
        require different processing—for example, items that require labels must be shipped separately from
        stickerless, commingled inventory.
        Args:
            ship_from_address:
            inbound_shipment_plan_request_items:
            ship_to_country_code:
            ship_to_country_ship_to_country_subdivision_code:
            label_prep_preference:
        Returns:
            :obj:`DictWrapper`
        """

        data = dict(Action='CreateInboundShipmentPlan',
                    ShipFromAddress=ship_from_address,
                    ShipToCountryCode=ship_to_country_code,
                    ShipToCountrySubdivisionCode=ship_to_country_ship_to_country_subdivision_code,
                    LabelPrepPreference=label_prep_preference
                    )
        data.update(enumerate_list('InboundShipmentPlanRequestItems.member.',
                                   inbound_shipment_plan_request_items))

        return self.make_request(data)

    def create_inbound_shipment(self, shipment_id, inbound_shipment_header, inbound_shipment_items):
        """
        Args:
            shipment_id:
            inbound_shipment_header:
            inbound_shipment_items:
        Returns:
            :obj:`DictWrapper`
        """
        data = dict(Action='CreateInboundShipment',
                    ShipmentId=shipment_id)
        data.update(enumerate_dict('InboundShipmentHeader', inbound_shipment_header))
        data.update(enumerate_dict('InboundShipmentItems', inbound_shipment_items))
        return self.make_request(data)


class OutboundShipments(mws.MWS):

    """ Amazon MWS OutboundShipments API """

    URI = "/FulfillmentOutboundShipment/2010-10-01"
    VERSION = "2010-10-01"
    NAMESPACE = '{http://mws.amazonaws.com/FulfillmentOutboundShipment/2010-10-01/}'
    NEXT_TOKEN_OPERATIONS = [
        'ListAllFulfillmentOrders',
    ]

    @next_token_action('ListAllFulfillmentOrders')
    def list_all_fulfillment_orders(self, query_start_date_time, next_token=None):
        data = dict(Action='ListAllFulfillmentOrders',
                    QueryStartDateTime=query_start_date_time)
        return self.make_request(data, "POST")

    def get_fulfillment_order(self, seller_fulfillment_order_id):
        data = dict(Action='GetFulfillmentOrder',
                    SellerFulfillmentOrderId=seller_fulfillment_order_id)
        return self.make_request(data, "POST")
