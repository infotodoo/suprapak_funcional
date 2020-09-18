# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessDenied
from datetime import datetime
import math
import logging

_logger = logging.getLogger(__name__)


class DataSheetSheet(models.Model):
    _name = 'data.sheet.sheet'
    _description = 'Data sheet sheet'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    sheet_id = fields.Many2one('data.sheet', 'Sheet', required=True)
    id_sheet = fields.Many2one('data.sheet', 'Sheet', required=True)
    id_char = fields.Char('Sheet id')
    repeat_id = fields.Many2one('repeat', 'Repeat')
    repetition = fields.Integer('Repetition', default=1.00)
    description = fields.Char('Description')


class DataSheetLine(models.Model):
    _name = 'data.sheet.line'
    _description = 'Data sheet line'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    product_qty = fields.Float('Quantity', digits=(12,12), default=1.00)
    uom_id = fields.Many2one('uom.uom', 'Unit of measure', digits='Product Price')
    standard_price = fields.Float('Unit Price', digits='Product Price')
    total = fields.Float('Total', readonly=True, compute='_compute_total',digits=(12,12))
    uom_categ_id = fields.Many2one('uom.category', 'Uom category')
    field_char = fields.Char('Field', default='None')
    field_product = fields.Char()
    # print.color
    press = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], 'U.Press')
    percentage = fields.Float('Participation')
    line = fields.Selection([('bs', 'BS'), ('ba', 'BA'), ('uv', 'UV')], 'Line')
    lineatura = fields.Char('Lineatura')
    bcm = fields.Float('BCM')
    # One2many
    sheet_id = fields.Many2one('data.sheet', 'Sheet')
    cold_foil_id = fields.Many2one('data.sheet', 'Cold Foil')
    print_color_id = fields.Many2one('data.sheet', 'Sheet')
    roll_id = fields.Many2one('data.sheet', 'Sheet')
    for_bag_id = fields.Many2one('data.sheet', 'Sheet')
    for_superlon_id = fields.Many2one('data.sheet', 'Sheet')
    refile_id = fields.Many2one('data.sheet', 'Sheet')
    revision_id = fields.Many2one('data.sheet', 'Sheet')
    print_id = fields.Many2one('data.sheet', 'Sheet')
    gluped_id = fields.Many2one('data.sheet', 'Sheet')
    gluped2_id = fields.Many2one('data.sheet', 'Sheet')
    movie_type_product_id = fields.Many2one('data.sheet', 'Sheet')
    rebobine_id = fields.Many2one('data.sheet', 'Sheet')
    pantone_id = fields.Many2one('pantone.print','Pantone')
    name_pantone = fields.Char('Pantone')
    participation_pantone = fields.Float('Pantone Participation')
    
    @api.depends('product_id')
    def _compute_total(self):
        for record in self:
            if record.product_id:
                record.uom_id = record.product_id.uom_id
                record.uom_categ_id = record.product_id.uom_id.category_id
                record.standard_price = record.product_id.standard_price
                record.total = record.standard_price * record.product_qty
            else:
                record.uom_id = None
                record.uom_categ_id = None
                record.standard_price = 0
                record.total = 0

    @api.onchange('product_qty')
    def _onchange_total(self):
        if self.product_qty and self.standard_price:
            self.total = self.standard_price * self.product_qty
        else:
            self.total = 0

    @api.onchange('field_product')
    def _onchange_field_product(self):
        self.field_product = self.product_id.tipo_producto
        if self.product_id:
            self.field_product = self.product_id.tipo_producto


def create(default=None):
    default['version_datetime'] = fields.Datetime.now()
    return True


class DataSheet(models.Model):
    _name = 'data.sheet'
    _description = 'Data sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    def _compute_production_ids(self):
        mp_obj = self.env['mrp.production']
        ids = self.bom_ids.ids
        mp = mp_obj.search([('bom_id', 'in', ids)])
        self.production_ids = mp

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    opportunity_id = fields.Many2one('crm.lead', 'Opportunity')
    state = fields.Selection([('draft', 'Quote sheet'), ('sample', 'Sample Tab'),
                              ('order', 'Order Tab')],
                             'state', copy=False, tracking=True)
    type_sheet = fields.Selection(
        [('review', 'Review'), ('technical', 'Technical Approval'), ('design', 'Design approval'),
         ('approved', 'Approved'), ('rejected', 'Rejected'), ('obsolete', 'Obsolete'),
         ('rejected_t', 'Rejected Technical'), ('rejected_d', 'Rejected Design')], 'Type sheet', tracking=True)
    name = fields.Char('Name')
    # Version
    version = fields.Integer('Version', default=1, required=True)
    product_id = fields.Many2one('product.product', 'Product')
    produce = fields.Char('produce', related='product_id.customer_reference')
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], 'Priority')
    # Info Customer
    partner_id = fields.Many2one('res.partner', 'Customer')
    parent_id = fields.Char('Subcustomer', related='partner_id.parent_id.name')
    commentary = fields.Char('Commentary')
    product_code = fields.Char('Product code', help='Customer product code')
    sector_id = fields.Many2one('res.sector', 'Sector')
    sector = fields.Char('Sector')
    team_id = fields.Many2one('crm.team', 'Zone')
    currency_id = fields.Many2one('res.currency', 'Currency')
    # sheet line
    line_ids = fields.One2many('data.sheet.line', 'sheet_id', 'Bills of Materials')
    # One2many
    print_color_ids = fields.One2many('data.sheet.line', 'print_color_id', 'Color')
    print_area_percentage = fields.Float('Print Area Percentage')
    roll_ids = fields.One2many('data.sheet.line', 'roll_id', 'Rolls')
    for_bag_ids = fields.One2many('data.sheet.line', 'for_bag_id', 'Bag')
    for_superlon_ids = fields.One2many('data.sheet.line', 'for_superlon_id', 'Superlon')
    refile_ids = fields.One2many('data.sheet.line', 'refile_id', 'Refile')
    revision_ids = fields.One2many('data.sheet.line', 'revision_id', 'Revision')
    print_ids = fields.One2many('data.sheet.line', 'print_id', 'Print')
    gluped_ids = fields.One2many('data.sheet.line', 'gluped_id', 'Gluped 1 to 2')
    gluped2_ids = fields.One2many('data.sheet.line', 'gluped2_id', 'Gluped 2 to 3')
    movie_type_product_ids = fields.One2many('data.sheet.line', 'movie_type_product_id', 'Movie')
    rebobine_ids = fields.One2many('data.sheet.line', 'rebobine_id', 'Rebobine')
    # Info Tec
    print_class = fields.Selection([('external', 'External'), ('internal', 'Internal')], 'Print Class')
    print_type_id = fields.Many2one('print.type', 'Print Type')
    uom_id = fields.Many2one('uom.uom', 'Unit of measure')
    product_type_id = fields.Many2one('data.product.type', 'Product line')
    drawn_type_id = fields.Many2one('data.drawn.type', 'Draw type')
    drawn_pass_id = fields.Many2one('drawn.pass', 'Draw Pass')
    movie_type_real_id = fields.Many2one('data.movie','Movie Type')
    movie_type_id = fields.Many2one('data.movie.type', 'Compound Code')
    movie_type_products_ids = fields.Many2many('product.product', 'sheet_product_rel', 'sheet_id', 'product_id',
                                               'Movie')
    color_movie_id = fields.Many2one('data.movie.color', 'Color movie')
    color_movie_id_1 = fields.Many2one('product.product', 'Color movie')
    sellalit_glue = fields.Many2one('product.product','Sellalit Glue')
    chemical_composition = fields.Many2one('chemical.composition', 'Chemical Composition')
    # Info cant
    specification_width_id = fields.Many2one('specification.width', 'Specification width')
    specification_width_name = fields.Float('Long Planned')
    specification_width_planned = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], 'Width Planned')
    specification_long_id = fields.Many2one('specification.long', 'Specification long')
    caliber_id = fields.Many2one('data.caliber.type', 'Specification caliber')
    tolerance_width = fields.Float('Tolerance width', compute='_compute_specification_width_id')
    tolerance_long = fields.Float('Tolerance long', compute='_compute_specification_long_id')
    tolerance_caliber = fields.Float('Tolerance caliber', compute='_compute_caliber_id')
    # Bool
    tongue = fields.Boolean('Tongue')
    thermal_adhesive = fields.Boolean('Thermal adhesive')
    print = fields.Boolean('Print')
    no_print = fields.Boolean('Without Print')
    rhombus = fields.Boolean('Rhombus')
    guillotine = fields.Boolean('Requires Guillotine')
    guillotine_mm = fields.Float('mm')
    # Comments
    comments = fields.Text('Comments')
    # Button
    quotation_count = fields.Integer(compute='_compute_sale_data', string="Number of Quotations")
    quantity = fields.Char(compute='_compute_quantity')
    #quantity ordered
    quantity_ordered = fields.Integer('Quantity',compute='_compute_quantity_ordered')
    order_ids = fields.One2many('sale.order', 'sheet_id', string='Orders')
    photo = fields.Binary()
    tag_form_id = fields.Many2one('data.tag.form', 'Tag Form')
    tag_color_id = fields.Many2one('data.movie.color', 'Tag Color')
    material_id = fields.Many2one('data.material', 'Material')
    application_id = fields.Many2one('data.application.mode', 'Application Mode')
    position_id = fields.Many2one('data.application.position', 'Application Position')
    content_id = fields.Char('Package Contents')
    form_id = fields.Many2one('data.form', 'Form')
    overlap_id = fields.Many2one('width.overlap', 'Width Overlap')
    tolerance_overlap = fields.Float('Tolerance Overlap', compute='_compute_overlap_id')
    overlap_location_id = fields.Many2one('overlap.location', 'Overlap Location')
    bom_id = fields.Many2one('mrp.bom', 'Actual BOM')
    bom_ids = fields.One2many('mrp.bom', 'sheet_id', 'Record')
    routing_id = fields.Many2one('mrp.routing', 'Routings')
    routings_ids = fields.Many2many('mrp.routing', 'sheet_routing_rel', 'sheet_id', 'routing_id', 'Routing')
    average_label_weight = fields.Float('Average Lable Weight', compute='_compute_average_label_weight',digits=(6,8))
    roll_weight = fields.Float('Roll Weight', compute='_compute_roll_weight')
    presentation_id = fields.Many2one('presentation', 'Presentation')
    presentation = fields.Char()
    meter_per_roll = fields.Char('Meters per roll')
    core_diameter_id = fields.Many2one('core.diameter', 'Core Diameter')
    embossing_number_id = fields.Many2one('embossing.number', 'Embossing Number')
    number_splices_id = fields.Many2one('number.splices', 'Number Splices')
    splice_type_id = fields.Many2one('splice.type', 'Splice Type')
    splicing_tape_id = fields.Many2one('splicing.tape', 'Splicing tape')
    seal_type_id = fields.Many2one('seal.type', 'Seal Type')
    sealing_tab = fields.Float('Sealing Tab')
    seal = fields.Char()
    mold_id = fields.Many2one('preformed', 'Mold')
    bottom_diameter = fields.Float('Bottom Diameter')
    upper_diameter = fields.Float('Upper Diameter')
    tab_length = fields.Float('Tab Length')
    band_height = fields.Float('Band Height')
    product = fields.Char('Product')
    long_modification = fields.Float('Long Modification')
    barcode_type_id = fields.Many2one('barcode.type', 'Barcode Type')
    barcode_number = fields.Char('Number')
    mechanic_plan_id = fields.Many2one('mechanic.plan')
    mechanic_plan_ids = fields.Many2many('mechanic.plan', 'sheet_mechanic_rel', 'sheet_id', 'mechanic_id',
                                         'Mechanic Plan')
    # Montaje multiple
    multiple_mount = fields.Boolean('This data have multiple Mount?')
    sheet_ids = fields.One2many('data.sheet.sheet', 'sheet_id', 'Multiple mount')
    microperforated = fields.Boolean('Microperforated')
    microperforated_id = fields.Many2one('microperforated')
    microperforated_ids = fields.Many2many('microperforated', 'sheet_microperfored_rel', 'sheed_id', 'microperfored_id',
                                           'Microperfored')
    drawn = fields.Boolean('Drawn')
    drawn_presentation_id = fields.Many2one('drawn.presentation', 'Drawn Presentation')
    waistband = fields.Boolean('Waistband')
    rod_number = fields.Integer('Rod Number')
    rod_adhesive_id = fields.Many2one('product.product', 'Rod Adhesive')
    print_adhesive_id = fields.Many2one('product.product', 'Print Adhesive')
    photo_format = fields.Binary('Photo Format')
    adhesive_type_id = fields.Many2one('adhesive.type', 'Adhesive Type')
    adhesive_type_selector = fields.Char()
    cold_foil = fields.Boolean('Cold Foil')
    cold_foil_id = fields.Many2one('cold.foil', 'Cold Foil Type')
    cold_foil_ids = fields.One2many('data.sheet.line','cold_foil_id','Cold Foil Type')
    cold_foil_selector = fields.Char()
    cold_foil_width = fields.Integer('Cold Foil Width')
    cast = fields.Boolean('Cast & Cure')
    cast_reference = fields.Char('Reference')
    cast_product_id = fields.Many2one('product.product','Cast & Cure')
    cast_width = fields.Char('Width Cast & Cure')
    ink_ids = fields.Many2many('inks', 'sheet_inks_rel', 'shhet_id', 'inks_id', 'Inks')
    required_match_print = fields.Boolean('required match Print')
    designer = fields.Many2one('designer', 'Designer')
    color_scale_id = fields.Many2one('color.scale', 'Color scale/check mark')
    complexity = fields.Selection([('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')], help="""Baja: Et. Sin imp o 
    Et imp de 1 a 3 colores planos"\nMedia: preformado o sellado sin impresión o ETPL básica (6 colores) o 
    cosmetico full color o ETPL basica + 1 pantone\nAlta: preformado o sellado impresos o Materiales Gillotinados 
    ET con mas de 1 pantone, ETPL con efectos especiales(varios pantone, cold foil, plata espejo, cast & cure, barnices,
     reproceso)""")
    control_change_id = fields.Many2one('control.change')
    control_changes_ids = fields.Many2many('control.change', 'sheet_control_rel', 'sheet_id', 'control_change_id')
    change_observation = fields.Char('Observations')
    separator_id = fields.Many2one('product.product', 'Separator')
    core_diameter = fields.Char('Core Diameter')
    width_core = fields.Float('Width Core')
    bag = fields.Many2one('product.product', 'Bag')
    box = fields.Many2one('product.product', 'Box')
    superlon = fields.Many2one('product.product', 'Superlon')
    tape_id = fields.Many2one('tape', 'Tape')  # depende ROLLO....
    plane_art = fields.Binary('Plane Art')
    funtional_test = fields.Binary('Funtional Test')
    repeat_id = fields.Many2one('repeat', 'Roller')
    room_large = fields.Char('Room Large', compute='_compute_specification_long_id')
    large_planned = fields.Char('Large Planned', compute='_compute_specification_long_id')
    gluped_id = fields.Many2one('product.product')
    for_rolls_ids = fields.Many2many('product.product', 'sheet_gluped_rel', 'sheet_id', 'gluped_id', 'For Rolls')
    for_bags_ids = fields.Many2many('product.product', 'sheet_gluped_rel', 'sheet_id', 'gluped_id', 'For Bags')
    for_superlon_id = fields.Many2one('product.product')
    rebobine_id = fields.Many2one('product.product')
    for_superlons_ids = fields.Many2many('product.product', 'sheet_superlon_rel', 'sheet_id', 'for_superlon_id',
                                         'For Superlon')
    for_box = fields.Selection([('supra', 'SUPRAPAK 2" 100 m BLANCA'), ('supra2', 'SUPRAPAK 2" 100 m TRANSPARENTE')],
                               'For Box')
    refiles_ids = fields.Many2many('product.product', 'sheet_gluped_rel', 'sheet_id', 'gluped_id', 'Tapes')
    revisions_ids = fields.Many2many('product.product', 'sheet_gluped_rel', 'sheet_id', 'gluped_id', 'Revisión')
    glupeds_ids = fields.Many2many('product.product', 'sheet_gluped_rel', 'sheet_id', 'gluped_id', 'Gluped 1 to 2')
    glupeds2_ids = fields.Many2many('product.product', 'sheet_gluped_rel', 'sheet_id', 'gluped_id', 'Gluped 3 to 4')
    rebobine = fields.Many2many('product.product', 'sheet_rebobine_rel', 'sheet_id', 'rebobine_id', 'Rebobine')
    # Production
    production_ids = fields.One2many('mrp.production', 'sheet_id', 'Productions', compute='_compute_production_ids')
    match_print_ids = fields.One2many('match.print.line', 'match_print_id', 'Match Print')

    # variables para domain
    largo = fields.Char('largo')
    largo2 = fields.Float('largo2')
    transversal = fields.Char('Transversal', compute='_compute_movie_type_id')
    longitudinal = fields.Char('Longitudinal', compute='_compute_movie_type_id')

    # nuevos cambios
    description_tag = fields.Char('Description Tag')
    ubicaition_label = fields.Char('Ubicaition Label')
    long_drawn_pass = fields.Integer('Long Drawn Pass')
    cross_drawn_pass = fields.Integer('Cross Drawn Pass')
    long_partial = fields.Integer('Long Partial')
    separation = fields.Boolean('Separation')
    planned_witdh = fields.Char('Planned Width', compute='_compute_planned_width')
    zip = fields.Char('Customer Code', compute='_compute_zip')
    unit_per_box = fields.Float('Unit per box', compute='_compute_unit_per_box')
    unit_per_bag = fields.Float('Unit per bag')
    separator = fields.Float ('Quantity Separator')
    adhesive_label_box = fields.Many2one('product.product', 'adhesive label box')
    adhesive_label = fields.Many2one('product.product', 'adhesive label bag')
    version_datetime = fields.Datetime('Datetime Version', default=fields.Datetime.now())

    # cambios excel
    production_waste_ids = fields.One2many('waste.production', 'sheet_id', 'Production and Scrap')
    waste_ids = fields.One2many('waste.production', 'sheet_id', 'Scrap')
    waste_total = fields.Float('Total Scrap', compute='_compute_waste_total',digits=(6,6))
    length_order = fields.Float('Order Length',compute='_compute_length_order',digits=(6,6))
    length_waste = fields.Float('Scrap Length', compute='_compute_length_waste')
    printer = fields.Char('Printer', compute='_compute_printer')
    blade_width = fields.Float('Blade Width', compute='_compute_blade_width',digits=(6,6))
    area_per_unit = fields.Float('Area per Unit', compute='_compute_area_per_unit',digits=(6,6))
    total_area_cold_foil = fields.Float(compute='_compute_total_area_cold_foil',digits=(6,8))
    total_area_cold_foil_1 = fields.Float('Total Area Cold Foil', compute='_compute_total_area_cold_foil_1',digits=(10,10))
    nazdar_adhesive_id = fields.Many2one('product.product','Nazdar Adhesive')
    weigth_roll = fields.Float('Weigth Roll (Kg)', compute='_compute_weigth_roll',digits=(6,6))
    unit = fields.Char(compute='_compute_unit')
    uds_m = fields.Float('Uds/m', compute='_compute_uds_m',digits=(6,6))
    uds_roll = fields.Float('Uds/roll',compute='_compute_uds_roll',digits=(6,6))
    weigth_m = fields.Float('Weigth/m',compute='_compute_weigth_m',digits=(6,6))
    uds_kg = fields.Float('Uds/Kg', compute="_compute_uds_kg",digits=(6,6))
    total_rolls = fields.Float(compute='_compute_total_rolls',digits=(6,6))
    total_rolls_1 = fields.Float('Total Rolls', compute='_compute_total_rolls_1',digits=(6,6))
    required_meters = fields.Float(compute='_compute_required_meters',digits=(6,6))
    required_meters_1 = fields.Float('Required Meters',compute='_compute_required_meters_1',digits=(6,6))
    meters_scrap = fields.Float(compute='_compute_meters_scrap',digits=(6,6))
    meters_scrap_1 = fields.Float('Meters with Scrap', compute='_compute_meters_scrap_1',digits=(6,12))
    total_weigth = fields.Float(compute='_compute_total_weigth',digits=(6,6))
    total_weigth_1 = fields.Float('Total Weigth', compute='_compute_total_weigth_1',digits=(6,6))
    total_weigth_scrap = fields.Float(compute='_compute_total_weigth_scrap',digits=(6,6))
    total_weigth_scrap_1 = fields.Float('Total Weigth with Scrap',compute='_compute_total_weigth_scrap_1',digits=(6,6))
    bag_to_box = fields.Integer('Bag by Box', compute='_compute_bag_to_box')
    user_id = fields.Many2one('res.users', 'Responsible', compute='_compute_user_id')

    # constants
    constant_minimun_meter = fields.Integer('Minimal Meters',default=3000)
    constant_adhesive = fields.Float('Constant Adhesive',digits=(12,12),default=0.000054945)
    constant_glue = fields.Float('Constant Glue',digits=(12,12),default=0.00000733)
    constant_squart_meter = fields.Float('Squares Meters',default=0.66)
    constant_ink = fields.Float('Ink Constant',default=0.45)
    constant_movie = fields.Float('Movie Constant',default=0.44)

    weigth_per_unit = fields.Float(compute='_compute_weigth_per_unit',digits=(6,6))

    quantity_unit = fields.Float(compute='_compute_quantity_unit')
    
    def _compute_quantity_ordered(self):
        self.quantity_ordered = int(self.quantity_unit)
    
    def _compute_quantity(self):
        self.quantity = 1
    
    @api.depends('quantity_ordered','constant_minimun_meter')
    def _compute_quantity_unit(self):
        if self.uom_id.name == 'Unidades' and self.uds_m != 0:
            pre_quantity = math.ceil(self.uds_m*self.constant_minimun_meter)
            pos = int(pre_quantity/100)+1
            quantity = pos * 100
            self.quantity_unit = quantity
        else:
            self.quantity_unit = 0

    def _compute_weigth_per_unit(self):
        if self.average_label_weight and self.uom_id.name == 'Unidades':
            self.weigth_per_unit = self.average_label_weight
        elif self.average_label_weight and self.uom_id.name == 'ROL':
            self.weigth_per_unit = self.roll_weight
        else:
            self.weigth_per_unit = 0
        """"if self.movie_type_real_id:
            if self.movie_type_real_id.name == 'OPS' and self.uom_id.name =='Unidades':
                self.weigth_per_unit = self.specification_width_id.name+(self.overlap_id.name/2)*100*self.specification_long_id.name*(self.caliber_id.name*self.constant_movie)*self.movie_type_real_id.density/1000
            elif self.movie_type_real_id.name == 'PLA' and self.uom_id.name =='Unidades':
                self.weigth_per_unit = (self.specification_width_id.name+self.overlap_id.name/2*100)*self.specification_long_id.name*(self.caliber_id.name*self.constant_movie)*self.movie_type_real_id.density/1000
            elif self.movie_type_real_id.name == 'PET' and self.uom_id.name =='Unidades':
                self.weigth_per_unit = (self.specification_width_id.name+self.overlap_id.name/2*100)*self.specification_long_id.name*(self.caliber_id.name*self.constant_movie)*self.movie_type_real_id.density/1000
            else:
                self.weigth_per_unit = (self.specification_width_id.name+self.overlap_id.name/2)*(self.specification_long_id.name+self.sealing_tab)*(self.caliber_id.name*self.constant_movie)*self.movie_type_real_id.density/1000/(self.sheet_ids if len(self.sheet_ids) > 1 else 1)"""

    # ultimate order in sheet
    order_after = fields.Many2one('sale.order', 'Ultimate order')

    def _compute_length_order(self):
        if self.uom_id.name == 'Unidades' and self.uds_m!= 0:
            self.length_order = int(self.quantity)/self.uds_m
        elif self.uom_id.name == 'ROL' and self.meter_per_roll:
            self.length_order = int(self.quantity)/int(self.meter_per_roll)
        else:
            self.length_order = 0

    @api.depends('uom_id')
    def _compute_total_weigth_scrap(self):
        if self.weigth_per_unit and self.quantity:
            self.total_weigth_scrap = self.weigth_per_unit*int(self.quantity)/1000*(self.waste_total/100)+self.weigth_per_unit*int(self.quantity)/1000
        else:
            self.total_weigth_scrap = 0

    @api.depends('uom_id')
    def _compute_total_weigth_scrap_1(self):
        if self.weigth_per_unit and self.quantity_ordered != 0:
            self.total_weigth_scrap_1 = self.weigth_per_unit*self.quantity_ordered/1000*(self.waste_total/100)+self.weigth_per_unit*self.quantity_ordered/1000
        else:
            self.total_weigth_scrap_1 = 0

    @api.depends('uom_id')
    def _compute_weigth_m(self):
        if self.uom_id.name == 'Unidades':
            self.weigth_m = self.uds_m*self.weigth_roll
        elif self.meter_per_roll != 0 and self.uom_id.name != 'Unidades':
            self.weigth_m = self.weigth_roll/int(self.meter_per_roll)*1000
        else:
            self.weigth_m = 0

    @api.depends('uom_id')
    def _compute_uds_roll(self):
        if self.uom_id.name == 'ROLLO' and self.specification_width_id.name != 0:
            self.uds_roll = math.floor(self.specification_long_id.name/self.specification_width_id.name)
        else:
            self.uds_roll = 0

    @api.depends('uom_id')
    def _compute_weigth_roll(self):
        if self.presentation_id.name == 'Unidades' and len(self.sheet_ids) > 0:
            self.weigth_roll = (self.specification_width_id.name+self.overlap_id.name/2)*(self.specification_long_id.name+self.sealing_tab)*(self.caliber_id.name*0.04)*self.movie_type_real_id.density/1000/len(self.sheet_ids)
        elif self.presentation_id.name == 'Unidades' and len(self.sheet_ids) == 0:
            self.weigth_roll = (self.specification_width_id.name+self.overlap_id.name/2)*(self.specification_long_id.name+self.sealing_tab)*(self.caliber_id.name*0.04)*self.movie_type_real_id.density/1000/1
        else:
            self.weigth_roll = ((self.specification_width_id.name+self.overlap_id.name/2)*(self.specification_long_id.name+self.sealing_tab)*(self.caliber_id.name*0.04)*self.movie_type_real_id.density/1000/1)/1000

    @api.depends('uom_id')
    def _compute_uds_kg(self):
        if self.uom_id.name == 'Unidades' and self.average_label_weight:
            self.uds_kg = (1000/self.average_label_weight)
        elif self.weigth_roll != 0:
            self.uds_kg = 1/self.weigth_roll
        else:
            self.uds_kg = 0


    @api.depends('uom_id')
    def _compute_required_meters(self):
        for record in self:
            if record.uom_id.name == 'Unidades':
                if record.uds_m != 0:
                    record.required_meters = int(record.quantity)/record.uds_m
                else:
                    record.required_meters = 0
            else:
                record.required_meters = int(record.quantity)*record.meter_per_roll

    @api.depends('uom_id')
    def _compute_required_meters_1(self):
        for record in self:
            if record.uom_id.name == 'Unidades':
                if record.uds_m != 0:
                    record.required_meters_1 = record.quantity_ordered/record.uds_m
                else:
                    record.required_meters_1 = 0
            else:
                record.required_meters_1 = record.quantity_ordered*record.meter_per_roll

    @api.depends('uom_id')
    def _compute_total_rolls(self):
        for record in self:
            if record.uom_id.name == 'Unidades':
                if record.uds_m != 0:
                    record.total_rolls =  int(record.quantity)/record.uds_m
                else:
                    record.total_rolls = 0
            else:
                record.total_rolls = int(record.quantity)*record.meter_per_roll

    @api.depends('uom_id')
    def _compute_total_rolls_1(self):
        for record in self:
            if record.uom_id.name == 'Unidades':
                if record.uds_m != 0:
                    record.total_rolls_1 =  record.quantity_ordered/record.uds_m
                else:
                    record.total_rolls_1 = 0
            else:
                record.total_rolls_1 = record.quantity_ordered*record.meter_per_roll

    @api.depends('uom_id')
    def _compute_uds_m(self):
        for record in self:
            if record.uom_id.name == 'Unidades' and record.specification_long_id:
                record.uds_m = 1000 / (record.specification_long_id.name
                                           + record.sealing_tab + record.guillotine_mm)
            elif record.uom_id.name == 'ROLLO' and record.specification_long_id:
                record.uds_m = 1000 / (record.specification_long_id.name
                                           + record.sealing_tab + record.guillotine_mm)
            else:
                record.uds_m = 0.0

    def _compute_user_id(self):
        self.user_id = self.env.user.id
        self.update({
            'user_id': self.user_id
        })

    @api.depends('presentation_id')
    def _compute_bag_to_box(self):
        for record in self:
            if record.presentation_id.name == 'ROLLO':
                record.bag_to_box = 1
            else:
                record.bag_to_box = 0

    @api.depends('uom_id')
    def _compute_total_weigth(self):
        if self.weigth_roll and self.quantity and self.uom_id.name == 'ROL':
            self.total_weigth = (self.weigth_roll * int(self.quantity)) / 1000
        elif self.uom_id.name =='Unidades' and self.quantity and self.average_label_weight:
            self.total_weigth = (self.average_label_weight * int(self.quantity)) / 1000
        else:
            self.total_weigth = 0

    @api.depends('uom_id')
    def _compute_total_weigth_1(self):
        if self.weigth_roll and self.quantity and self.uom_id.name == 'ROL':
            self.total_weigth_1 = (self.weigth_roll * self.quantity_ordered) / 1000
        elif self.uom_id.name =='Unidades' and self.quantity and self.average_label_weight:
            self.total_weigth_1 = (self.average_label_weight * self.quantity_ordered) / 1000
        else:
            self.total_weigth_1 = 0

    @api.depends('waste_total', 'required_meters')
    def _compute_meters_scrap(self):
        if self.waste_total and self.required_meters:
            self.meters_scrap = self.required_meters / (1 - (self.waste_total/100))
        else:
            self.meters_scrap = 0
            
    @api.depends('waste_total', 'required_meters_1')
    def _compute_meters_scrap_1(self):
        if self.waste_total and self.required_meters_1:
            self.meters_scrap_1 = self.required_meters_1 / (1 - (self.waste_total/100))
        else:
            self.meters_scrap_1 = 0

    @api.depends('uom_id.name')
    def _compute_unit(self):
        if self.uom_id.name == 'ROLLO':
            self.unit = 'KG'
        else:
            self.unit = 'gr'

    @api.depends('cold_foil_width', 'specification_long_id', 'quantity')
    def _compute_total_area_cold_foil(self):
        if self.cold_foil_width >= 60 and self.specification_long_id.name and self.quantity:
            self.total_area_cold_foil = ((((self.cold_foil_width + 3) / 1000) * self.specification_long_id.name
                                          / 1000)) * int(self.quantity)
        elif self.cold_foil_width < 60 and self.specification_long_id.name and self.quantity:
            self.total_area_cold_foil = ((((60 + 3) / 1000) * self.specification_long_id.name
                                          / 1000)) * int(self.quantity)
        else:
            self.total_area_cold_foil = 0

    @api.depends('cold_foil_width', 'specification_long_id.name', 'quantity_ordered')
    def _compute_total_area_cold_foil_1(self):
        if self.cold_foil_width > 60 and self.specification_long_id.name and self.quantity_ordered:
            self.total_area_cold_foil_1 = ((((self.cold_foil_width + 3) / 1000) * self.specification_long_id.name
                                          / 1000)) * self.quantity_ordered
        elif self.cold_foil_width < 60 and self.specification_long_id.name and self.quantity:
            self.total_area_cold_foil_1 = ((((60 + 3) / 1000) * self.specification_long_id.name
                                          / 1000)) * self.quantity_ordered
        else:
            self.total_area_cold_foil_1 = 0

    @api.depends('planned_witdh', 'specification_long_id.name', 'sealing_tab', 'guillotine_mm')
    def _compute_area_per_unit(self):
        if self.planned_witdh and self.specification_long_id.name:
            self.area_per_unit = float(self.blade_width) * ((self.specification_long_id.name + self.sealing_tab +
                                                      self.guillotine_mm) / 1000)
        else:
            self.area_per_unit = 0

    @api.depends('specification_width_id', 'overlap_id','specification_width_planned')
    def _compute_blade_width(self):
        if self.specification_width_planned and self.specification_width_id.name and self.overlap_id.name: #and self.color_scale_id.name:
            self.blade_width = ((((self.specification_width_id.name * 2) + self.overlap_id.name) * \
                                 int(self.specification_width_planned)) + self.color_scale_id.name) / 1000
        else:
            self.blade_width = 0

    @api.depends('waste_ids.operations', 'waste_ids.work_center', 'waste_ids.routing')
    def _compute_printer(self):
        for record in self:
            lis = []
            for waste in record.waste_ids:
                lis.append(waste.work_center)
            if 'SIAT' in lis:
                record.printer = 'SIAT'
            elif 'SIAT' not in lis and 'IBIRAMA 3' in lis:
                record.printer = 'IBIRAMA 3'
            elif 'SIAT' not in lis and 'IBIRAMA 3' not in lis and 'MK2200' in lis:
                record.printer = 'MK2200'
            else:
                record.printer = 'MK P5'

    @api.depends('meters_scrap')
    def _compute_length_waste(self):
        self.length_waste = self.meters_scrap
            
    @api.depends('waste_ids.routing', 'waste_ids.average')
    def _compute_waste_total(self):
        waste_total = 0
        for record in self:
            for waste in record.waste_ids:
                if waste.routing and waste.average:
                    waste_total += waste.average
        record.update({
            'waste_total': waste_total,
        })

    @api.onchange('movie_type_id')
    def _compute_chemical_composition(self):
        if self.movie_type_id:
            self.chemical_composition = self.movie_type_id.chemical_composition_id
        else:
            self.chemical_composition = None

    @api.depends('presentation_id', 'specification_width_id.name')
    def _compute_unit_per_box(self):
        for record in self:
            if record.average_label_weight and record.presentation_id.name in ('CORTADO', 'SELLADO'):
                if record.average_label_weight == 0.0:
                    record.unit_per_box = 0.0
                elif record.average_label_weight:
                    _box = (20.0 * 1000.0) / record.average_label_weight
                    per_box = int(_box) / 100
                    boxes = int(per_box) * 100
                    record.unit_per_box = boxes
            elif record.specification_width_id and record.presentation_id.name == 'PREFORMADO':
                if record.specification_width_id.name <= 50.0:
                    record.unit_per_box = 23000.0
                elif 50.0 < record.specification_width_id.name < 65.0:
                    record.unit_per_box = 12000.0
                elif 65.0 < record.specification_width_id.name < 95.0:
                    record.unit_per_box = 6000.0
                elif record.specification_width_id.name > 95.0:
                    record.unit_per_box = 3500.0
                elif record.partner_id and record.partner_id.bool_postobon:
                    record.unit_per_box = 5200.0
                else:
                    record.unit_per_box = 0.0
            else:
                record.unit_per_box = 0.0

    @api.onchange('presentation_id', 'specification_width_id')
    def _compute_unit_per_bag(self):
        for record in self:
            if record.specification_width_id:
                if record.partner_id and record.partner_id.bool_avon:
                    record.unit_per_bag = 1000.0
                elif record.specification_width_id.name >= 90.0:
                    record.unit_per_bag = 1000.0
                elif record.specification_width_id.name < 90.0:
                    record.unit_per_bag = 2000.0
                else:
                    record.unit_per_bag = 0.0
            else:
                record.unit_per_bag = 0.0

    @api.depends('partner_id')
    def _compute_zip(self):
        if self.partner_id:
            self.zip = self.partner_id.zip
        else:
            self.zip = None

    @api.depends('specification_width_id.name', 'overlap_id.name', 'color_scale_id.name')
    def _compute_planned_width(self):
        self.planned_witdh = (self.specification_width_id.name * 2) + self.overlap_id.name + \
                             self.color_scale_id.name

    def action_create_wizard_revision(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Solicitud de revisión de la ficha #' + record.name +
                       ' Hay una nueva elaboración o modificación a la ficha #' + record.name +
                       ' Diligenciada por:' + record.user_id.name +
                       ' Se requiere su ingreso al sistema para su revisión.',
            'users_ids': ids,
        }
        wiz_id = self.env['data.revision'].create(vals_wiz)
        action = imd.xmlid_to_object('suprapak_kronos.action_data_revision')
        form_view_id = imd.xmlid_to_res_id('suprapak_kronos.view_message_revision')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def action_create_wizard_technical(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Se acaba de revisar la ficha #' + record.name,
            'users_ids': ids,
        }
        wiz_id = self.env['data.technical'].create(vals_wiz)
        action = imd.xmlid_to_object('suprapak_kronos.action_data_technical')
        form_view_id = imd.xmlid_to_res_id('suprapak_kronos.view_message_technical')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def action_create_wizard_design(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Hay una nueva elaboración o modificación a la ficha diseño # ' + record.name
                       + ' Diligenciada por: ' + record.user_id.name +
                       ' Se requiere su ingreso al sistema para su revisión.',
            'users_ids': ids,
        }
        wiz_id = self.env['data.design'].create(vals_wiz)
        action = imd.xmlid_to_object('suprapak_kronos.action_data_design')
        form_view_id = imd.xmlid_to_res_id('suprapak_kronos.view_message_design')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def action_create_wizard_approved(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Se acaba de aprobar la ficha diseño # ' + record.name,
            'users_ids': ids,
        }
        wiz_id = self.env['data.approved'].create(vals_wiz)
        action = imd.xmlid_to_object('suprapak_kronos.action_data_approved')
        form_view_id = imd.xmlid_to_res_id('suprapak_kronos.view_message_approved')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def action_create_wizard_rejected(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Se acaba de rechazar la ficha diseño # ' + record.name,
            'users_ids': ids,
        }
        wiz_id = self.env['data.rejected'].create(vals_wiz)
        action = imd.xmlid_to_object('suprapak_kronos.action_data_rejected')
        form_view_id = imd.xmlid_to_res_id('suprapak_kronos.view_message_rejected')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def action_create_wizard_rejected_t(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Se acaba de rechazar la ficha diseño # ' + record.name,
            'users_ids': ids,
        }
        wiz_id = self.env['data.rejected.t'].create(vals_wiz)
        action = imd.xmlid_to_object('suprapak_kronos.action_data_rejected_t')
        form_view_id = imd.xmlid_to_res_id('suprapak_kronos.view_message_rejected_t')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def action_create_wizard_rejected_d(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Se acaba de rechazar la ficha diseño # ' + record.name,
            'users_ids': ids,
        }
        wiz_id = self.env['data.rejected.d'].create(vals_wiz)
        action = imd.xmlid_to_object('suprapak_kronos.action_data_rejected_d')
        form_view_id = imd.xmlid_to_res_id('suprapak_kronos.view_message_rejected_d')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def progressbar_review(self):
        self.type_sheet = 'review'
        res = self.action_create_wizard_revision()
        return res

    def progressbar_technical(self):
        self.type_sheet = 'technical'
        res = self.action_create_wizard_technical()
        return res

    def progressbar_design(self):
        self.type_sheet = 'design'
        res = self.action_create_wizard_design()
        return res

    def progressbar_approved(self):
        self.type_sheet = 'approved'
        res = self.action_create_wizard_approved()
        return res

    def progressbar_rejected(self):
        self.type_sheet = 'rejected'
        res = self.action_create_wizard_rejected()
        return res

    def progressbar_obsolete(self):
        self.type_sheet = 'obsolete'

    def progressbar_rejected_t(self):
        self.type_sheet = 'rejected_t'
        res = self.action_create_wizard_rejected_t()
        return res

    def progressbar_rejected_d(self):
        self.type_sheet = 'rejected_d'
        res = self.action_create_wizard_rejected_d()
        return res

    @api.depends('movie_type_id')
    def _compute_movie_type_id(self):
        if self.movie_type_id:
            self.transversal = self.movie_type_id.transversal
            self.longitudinal = self.movie_type_id.longitudinal
        else:
            self.transversal = None
            self.longitudinal = None

    @api.constrains('rod_number')
    def _check_rod_number(self):
        for record in self:
            if record.rod_number > 4:
                raise AccessDenied(("No puede superar 4"))

    @api.onchange('movie_type_real_id')
    def _onchange_movie_type_real_id(self):
        if self.movie_type_real_id:
            #self.largo = self.movie_type_id.movie_type
            self.movie_type_id.movie_type = self.movie_type_real_id.name
    
    @api.onchange('specification_long_id')
    def _onchange_specification_long_id(self):
        if self.specification_long_id:
            self.largo2 = self.repeat_id.large_planned
            self.repeat_id.large_planned = self.specification_long_id.name

    @api.depends('color_scale_id.name', 'specification_width_id.name', 'overlap_id.name')
    def _compute_specification_width_planned(self):
        self.specification_width_planned = self.overlap_id.name * 2 + self.specification_width_id.name \
                                           + self.color_scale_id.name

    @api.depends('specification_long_id')
    def _compute_specification_long_id(self):
        if self.specification_long_id:
            self.tolerance_long = self.specification_long_id.tolerance
            self.large_planned = self.specification_long_id.name
            self.room_large = self.specification_long_id.room_large
        else:
            self.tolerance_long = None
            self.large_planned = None
            self.room_large = None

    @api.onchange('width_core')
    def _onchange_width_core(self):
        if self.width_core:
            self.width_core += 4

    @api.onchange('presentation_id')
    def _onchange_presentation_id(self):
        if self.presentation_id:
            self.presentation = self.presentation_id.name

    @api.depends('specification_width_id.name', 'specification_long_id.name', 'overlap_id.name', 'guillotine_mm',
                 'movie_type_real_id.density','caliber_id.name', 'sealing_tab')
    def _compute_roll_weight(self):
        self.roll_weight = (self.specification_width_id.name + self.overlap_id.name / 2) * int(self.meter_per_roll) \
                           * (self.caliber_id.name * 0.04) * self.movie_type_real_id.density

    @api.depends('specification_width_id.name', 'specification_long_id.name', 'overlap_id.name', 'guillotine_mm',
                 'movie_type_real_id.density', 'caliber_id.name', 'sealing_tab')
    def _compute_average_label_weight(self):
        self.average_label_weight = (self.specification_width_id.name + self.overlap_id.name / 2) * (
                (self.specification_long_id.name + self.sealing_tab + self.guillotine_mm) *
                (self.caliber_id.name * 0.04) * self.movie_type_real_id.density) / 1000

    @api.onchange('seal_type_id')
    def _onchange_seal_type_id(self):
        if self.seal_type_id:
            self.seal = self.seal_type_id.name

    @api.depends('specification_width_id')
    def _compute_specification_width_id(self):
        if self.specification_width_id:
            self.tolerance_width = self.specification_width_id.tolerance
        else:
            self.tolerance_width = None

    @api.onchange('adhesive_type_id')
    def _oncahnge_adhesive_type_id(self):
        if self.adhesive_type_id:
            self.adhesive_type_selector = self.adhesive_type_id.name

    @api.onchange('cold_foil_id')
    def _oncahnge_cold_foil_id(self):
        if self.cold_foil_id:
            self.cold_foil_selector = self.cold_foil_id.name

    @api.onchange('mold_id')
    def _onchange_mold_id(self):
        if self.mold_id:
            self.bottom_diameter = self.mold_id.bottom_diameter
            self.upper_diameter = self.mold_id.upper_diameter
            self.tab_length = self.mold_id.tab_length
            self.band_height = self.mold_id.band_height
            self.product = self.mold_id.product

    @api.depends('overlap_id')
    def _compute_overlap_id(self):
        if self.overlap_id:
            self.tolerance_overlap = self.overlap_id.tolerance
        else:
            self.tolerance_overlap = None

    def _compute_sale_data(self):
        for lead in self:
            lead.quotation_count = len(lead.order_ids)

    """@api.onchange('movie_type_id')
    def _onchange_movie_type_id(self):
        if self.movie_type_id:
            self.color_movie_id = self.movie_type_id.color_id"""

    @api.depends('caliber_id')
    def _compute_caliber_id(self):
        if self.caliber_id:
            self.tolerance_caliber = self.caliber_id.tolerance
        else:
            self.tolerance_caliber = None

    

    #Bill of Material
    @api.onchange('print_color_ids')
    def _onchange_print_color_ids(self):
        values = []
        count = 0
        for lines in self.print_color_ids:#[count]:
            count +=1
            if self.quantity and self.print_area_percentage != 0 and lines.bcm != 0:
                weigth =(((self.specification_width_id.name*2+self.overlap_id.name)*int(self.specification_width_planned))+self.color_scale_id.name)/1000
                area = weigth*self.meters_scrap
                consumption = area*lines.bcm*self.constant_ink
                pre_quantity = consumption/1000/int(self.quantity)*(self.print_area_percentage/100)
                quantity = pre_quantity*(lines.percentage/100)
            elif self.quantity and self.print_area_percentage != 0 and lines.bcm and lines.name_pantone:
                weigth =(((self.specification_width_id.name*2+self.overlap_id.name)*int(self.specification_width_planned))+self.color_scale_id.name)/1000
                area = weigth*self.meters_scrap
                consumption = area*lines.bcm*self.constant_ink
                percentage_ink = (consumption/100)*(lines.percentage/100)
                pre_quantity = percentage_ink/int(self.quantity)*(self.print_area_percentage/100)
                quantity = pre_quantity*(lines.participation_pantone/100)
            else:
                quantity = 0
            dic = {
            'product_id': lines.product_id.id,
            'product_qty': quantity,
            'uom_id': lines.product_id.uom_id.id,
            'standard_price': lines.standard_price,
            'total': lines.standard_price*quantity,
            }
            flag = True
            for lm in self.line_ids:
                if lm.product_id == lines.product_id:
                    self.write({
                        'line_ids':[(1,lm.id,dic)]
                    })
                    flag = False
            if flag:
                values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('sellalit_glue')
    def _onchange_sellalit_glue(self):
        if self.constant_glue and self.constant_minimun_meter and self.quantity:
            quantity = self.constant_glue*self.meters_scrap #self.constant_minimun_meter)/int(self.quantity)
        else:
            quantity = 0
        values = []
        if self.sellalit_glue:
            self.line_ids.search([('field_char', '=', 'sellalit_glue')]).unlink()
            dic = {
                'field_char': 'sellalit_glue',
                'product_id': self.sellalit_glue.id,
                'product_qty': quantity,
                'uom_id': self.sellalit_glue.uom_id.id,
                'standard_price': self.sellalit_glue.standard_price,
                'total': self.sellalit_glue.standard_price * quantity,
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('nazdar_adhesive_id')
    def _onchange_nazdar_adhesive_id(self):
        if self.total_area_cold_foil and int(self.quantity) > 0:
            quantity = (self.total_area_cold_foil/1000)/int(self.quantity)
        else:
            quantity = 0
        values = []
        if self.nazdar_adhesive_id:
            self.line_ids.search([('field_char', '=', 'nazdar_adhesive_id')]).unlink()
            dic = {
                'field_char': 'nazdar_adhesive_id',
                'product_id': self.nazdar_adhesive_id.id,
                'product_qty': quantity,
                'uom_id': self.nazdar_adhesive_id.uom_id.id,
                'standard_price': self.nazdar_adhesive_id.standard_price,
                'total': self.nazdar_adhesive_id.standard_price * quantity,
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('cast_product_id')
    def _onchange_cast_product_id(self):
        if self.cast_width and self.quantity:
            total = ((int(self.cast_width)+3)/1000*self.specification_long_id.name)/1000
            pre_quantity = total*1.1*int(self.quantity)
            quantity = pre_quantity
        else:
            quantity = 0
        values = []
        if self.cast_product_id:
            self.line_ids.search([('field_char', '=', 'cast_product_id')]).unlink()
            dic = {
                'field_char': 'cast_product_id',
                'product_id': self.cast_product_id.id,
                'product_qty': quantity,
                'uom_id': self.cast_product_id.uom_id.id,
                'standard_price': self.cast_product_id.standard_price,
                'total': self.cast_product_id.standard_price * quantity,
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('print_adhesive_id')
    def _onchange_print_adhesive_id(self):
        quantity = (self.area_per_unit*int(self.quantity))*self.constant_squart_meter/1000
        values = []
        if self.print_adhesive_id:
            self.line_ids.search([('field_char', '=', 'print_adhesive_id')]).unlink()
            dic = {
                'field_char': 'print_adhesive_id',
                'product_id': self.print_adhesive_id.id,
                'product_qty': quantity,
                'uom_id': self.print_adhesive_id.uom_id.id,
                'standard_price': self.print_adhesive_id.standard_price,
                'total': self.print_adhesive_id.standard_price * quantity,
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('rod_adhesive_id')
    def _onchange_rod_adhesive_id(self):
        if self.rod_number and self.meters_scrap and self.constant_adhesive and self.quantity:
            quantity = (self.rod_number*self.meters_scrap*self.constant_adhesive)/int(self.quantity)
        else:
            quantity = 0
        values = []
        if self.rod_adhesive_id:
            self.line_ids.search([('field_char', '=', 'rod_adhesive_id')]).unlink()
            dic = {
                'field_char': 'rod_adhesive_id',
                'product_id': self.rod_adhesive_id.id,
                'product_qty': quantity,
                'uom_id': self.rod_adhesive_id.uom_id.id,
                'standard_price': self.rod_adhesive_id.standard_price,
                'total': self.rod_adhesive_id.standard_price * quantity,
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id

    @api.onchange('bag')
    def _onchange_bag(self):
        values = []
        if self.bag:
            pre_quantity = math.ceil(self.quantity_ordered/self.unit_per_bag)#int(self.quantity)/self.unit_per_bag
            quantity = pre_quantity/self.quantity_ordered
            self.line_ids.search([('field_char', '=', 'bag')]).unlink()
            dic = {
                'field_char': 'bag',
                'product_id': self.bag.id,
                'product_qty': quantity,
                'uom_id': self.bag.uom_id.id,
                'standard_price': self.bag.standard_price,
                'total': self.bag.standard_price*quantity,
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('separator_id')
    def _onchange_separator_id(self):
        values = []
        if self.separator_id:
            self.line_ids.search([('field_char', '=', 'separator_id')]).unlink()
            dic = {
                'field_char': 'separator_id',
                'product_id': self.separator_id.id,
                'product_qty': 1,
                'uom_id': self.separator_id.uom_id.id,
                'standard_price': self.separator_id.standard_price,
                'total': self.separator_id.standard_price,

            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})
    
    @api.onchange('movie_type_product_ids')
    def _onchange_movie_type_product_ids(self):
        values = []
        if self.movie_type_product_ids:
            for lines in self.movie_type_product_ids:
                dic = {
                'product_id': lines.product_id.id,
                'product_qty': self.total_weigth_scrap,
                'uom_id': lines.product_id.uom_id.id,
                'standard_price': lines.standard_price,
                'total': lines.standard_price*self.total_weigth_scrap,
                }
                flag = True
                for lm in self.line_ids:
                    if lm.product_id == lines.product_id:
                        self.write({
                            'line_ids':[(1,lm.id,dic)]
                        })
                        flag = False
                if flag:
                    values.append((0, 0, dic))
            if values:
                self.write({'line_ids': values})

    @api.onchange('cold_foil_ids')
    def _onchange_cold_foil_ids(self):
        if int(self.quantity) > 0:
            quantity = self.total_area_cold_foil/int(self.quantity)
        else:
            quantity = 0
        values = []
        if self.cold_foil_ids:
            for lines in self.cold_foil_ids:
                dic = {
                    'product_id': lines.product_id.id,
                    'product_qty': quantity,
                    'uom_id': lines.uom_id.id,
                    'standard_price': lines.product_id.standard_price,
                    'total': lines.product_id.standard_price * quantity,
                }
                flag = True
                for lm in self.line_ids:
                    if lm.product_id == lines.product_id:
                        self.write({
                            'line_ids':[(1,lm.id,dic)]
                        })
                        flag = False
                if flag:
                    values.append((0, 0, dic))
            if values:
                self.write({'line_ids': values})

    @api.onchange('color_movie_id_1')
    def _onchange_color_movie_id_1(self):
        if self.meters_scrap and self.quantity:
            quantity = self.meters_scrap/int(self.quantity)
        else:
            quantity = 0
        values = []
        if self.color_movie_id_1:
            self.line_ids.search([('field_char', '=', 'color_movie_id_1')]).unlink()
            dic = {
                'field_char': 'color_movie_id_1',
                'product_id': self.color_movie_id_1.id,
                'product_qty': quantity,
                'uom_id': self.color_movie_id_1.uom_id.id,
                'standard_price': self.color_movie_id_1.standard_price,
                'total': self.color_movie_id_1.standard_price*quantity,
            }
            values.append((0,0,dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('box')
    def _onchange_box(self):
        values = []
        if self.box:
            pre_quantity = math.ceil(self.quantity_ordered/self.unit_per_box)#int(self.quantity)/self.unit_per_box
            quantity = pre_quantity/self.quantity_ordered
            self.line_ids.search([('field_char', '=', 'box')]).unlink()
            dic = {
                'field_char': 'box',
                'product_id': self.box.id,
                'product_qty': quantity,
                'uom_id': self.box.uom_id.id,
                'standard_price': self.box.standard_price,
                'total': self.box.standard_price*quantity,
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('superlon')
    def _onchange_superlon(self):
        values = []
        if self.superlon:
            self.line_ids.search([('field_char', '=', 'superlon')]).unlink()
            dic = {
                'field_char': 'superlon',
                'product_id': self.superlon.id,
                'product_qty': 1,
                'uom_id': self.superlon.uom_id.id,
                'standard_price': self.superlon.standard_price,
                'total': self.superlon.standard_price,
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('roll_ids')
    def _roll_ids(self):
        for line in self.roll_ids:
            line.sheet_id = self

    @api.onchange('for_bag_ids')
    def _for_bag_ids(self):
        for line in self.for_bag_ids:
            line.sheet_id = self

    @api.onchange('for_superlon_ids')
    def _for_superlon_ids(self):
        for line in self.for_superlon_ids:
            line.sheet_id = self

    @api.onchange('refile_ids')
    def _refile_ids(self):
        for line in self.refile_ids:
            line.sheet_id = self

    @api.onchange('revision_ids')
    def _revision_ids(self):
        for line in self.revision_ids:
            line.sheet_id = self

    @api.onchange('gluped_ids')
    def _gluped_ids(self):
        for line in self.gluped_ids:
            line.sheet_id = self

    @api.onchange('gluped2_ids')
    def _gluped2_ids(self):
        for line in self.gluped2_ids:
            line.sheet_id = self

    @api.onchange('rebobine_ids')
    def _rebobine_ids(self):
        for line in self.rebobine_ids:
            line.sheet_id = self

    @api.onchange('print_ids')
    def _print_ids(self):
        for line in self.print_ids:
            line.sheet_id = self

    """def write(self, values):
        res = super(DataSheet, self).write(values)
        self.action_create_quotation()
        return res"""

    def copy(self, default=None):
        default = dict(default or {})
        default['version'] = self.version + 1
        default['version_datetime'] = fields.Datetime.now()
        res = super(DataSheet, self).copy(default)
        self.type_sheet = 'obsolete'
        return res

    def action_create_quotation(self):
        so_obj = self.env['sale.order']
        for record in self:
            if not record.partner_id:
                raise ValidationError("Por favor asignar un cliente")
            vals = {
                'product_id': record.product_id.id,
                'product_uom': record.uom_id.id,
                'product_uom_qty': record.quantity,
                'material_id': record.material_id.id,
                'drawn_type_id': record.drawn_type_id.id,
                'movie_type_id': record.movie_type_id.id,
                'specification_width': record.specification_width_id.id,
                'specification_long': record.specification_long_id.id,
                'caliber_id': record.caliber_id.id,
                'tongue': record.tongue,
                'thermal_adhesive': record.thermal_adhesive,
            }
            val = {
                'opportunity_id': record.opportunity_id.id if record.opportunity_id else None,
                'partner_id': record.partner_id.id,
                'origin': record.name,
                'company_id': self.company_id.id or self.env.company.id,
                'sheet_id': record.id,
                'order_line': [(0, 0, vals)],
            }
            so = so_obj.create(val)
            so.order_line.product_id_change()
            record.order_after = so

    def action_create_wizard(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Notificacion de nueva cotizacion de la ficha cotizacion: #' + record.order_after.name,
            'users_ids': ids,
        }
        wiz_id = self.env['create.quotation'].create(vals_wiz)
        action = imd.xmlid_to_object('suprapak_kronos.action_create_quotation')
        form_view_id = imd.xmlid_to_res_id('suprapak_kronos.view_message_activity')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def action_sale_quotations_new(self):
        self.action_create_quotation()
        if self.quotation_count:
            res = self.action_create_wizard()
        return res

    def action_new_quotation(self):
        action = self.env.ref("sale_crm.sale_action_quotations_new").read()[0]
        vals = {
            'product_id': self.product_id.id,
            'product_uom': self.uom_id.id,
            'material_id': self.material_id.id,
            'drawn_type_id': self.drawn_type_id.id,
            'movie_type_id': self.movie_type_id.id,
            'specification_width': self.specification_width_id.id,
            'specification_long': self.specification_long_id.id,
            'caliber_id': self.caliber_id.id,
        }
        action['context'] = {
            'search_default_opportunity_id': self.opportunity_id.id,
            'default_opportunity_id': self.opportunity_id.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_origin': self.name,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_sheet_id': self.id,
            'default_order_line': [(0, 0, vals)],
        }
        return action

    def action_view_sale_quotation(self):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_sheet_id': self.id
        }
        action['domain'] = [('sheet_id', '=', self.id)]
        quotations = self.mapped('order_ids')
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id
        return action

    def action_bom_line(self):
        mrp_object = self.env['mrp.bom']
        for record in self:
            valores = []
            for line in record.line_ids:
                dic = {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                    # 'standard_price': line.uom_id.id
                }
                valores.append((0, 0, dic))
            valor = {
                'product_tmpl_id': record.product_id.product_tmpl_id.id,
                'bom_line_ids': valores,
                'routing_id': record.routing_id.id,
                'sheet_id': record.id,
                'code': record.name or ''
            }
            record.bom_id = mrp_object.create(valor)
        return True


class WasteProduction(models.Model):
    _name = 'waste.production'
    _description = 'Waste and Production'

    sheet_id = fields.Many2one('data.sheet', 'Sheet')
    name = fields.Many2one('mrp.routing.workcenter', 'Operations')
    work_center_id = fields.Many2one('mrp.workcenter', 'Machines')
    routing = fields.Boolean('Routing')
    average_waste = fields.Float('Average Waste')
    operations = fields.Char('Operations', compute='_compute_waste')
    work_center = fields.Char('Machines', compute='_compute_waste')
    average = fields.Float('Average Waste', compute='_compute_waste')
    waste_total = fields.Float('Waste Total')
    quantity_entered = fields.Float('Quantity Material Entered',compute='_compute_quantity_entered')

    def _compute_quantity_entered(self):
        for record in self:
            if record.name.name == 'Slitter 4' and record.work_center_id.name == 'SLITTER 4':
                record.quantity_entered = record.sheet_id.length_waste
            else:
                record.quantity_entered = record.sheet_id.length_waste*(1-(100)/100) 

    @api.depends('name', 'work_center_id', 'average_waste')
    def _compute_waste(self):
        for record in self:
            if record.name and record.work_center_id and record.average_waste:
                record.operations = record.name.name
                record.work_center = record.work_center_id.name
                record.average = record.average_waste
            else:
                record.operations = None
                record.work_center = None
                record.average = 0


class DataProductType(models.Model):
    _name = 'data.product.type'
    _description = 'Product type'

    name = fields.Char('Name')
    code = fields.Char('Code')


class DataDrawType(models.Model):
    _name = 'data.drawn.type'
    _description = 'Drawing type'

    name = fields.Char('Name')
    code = fields.Char('Code')


class DataMovieColor(models.Model):
    _name = 'data.movie.color'
    _description = 'Colors'

    name = fields.Char('Color')
    code = fields.Char('Code')

class DataMovie(models.Model):
    _name = 'data.movie'
    _description = 'Movie Type'
    
    name = fields.Char('Name')
    density = fields.Float('Density', digits='Product Unit of Measure')

class DataMovieType(models.Model):
    _name = 'data.movie.type'
    _description = 'Compound Code'

    name = fields.Char('Name')
    movie_type = fields.Many2one('data.movie','Movie Type',required=True)
    color_id = fields.Many2one('data.movie.color', 'Color')
    transversal = fields.Char('Transversal')
    longitudinal = fields.Char('Longitudinal')
    chemical_composition_id = fields.Many2one('chemical.composition', 'Chemical Composition')


class DataCaliberType(models.Model):
    _name = 'data.caliber.type'
    _description = 'Caliber type'

    name = fields.Float('Caliber')
    code = fields.Char('Code')
    tolerance = fields.Float('Tolerance')


class DataForm(models.Model):
    _name = 'data.form'
    _description = 'Form'

    name = fields.Char('Form')
    code = fields.Char('code')


class DataTagForm(models.Model):
    _name = 'data.tag.form'
    _description = 'Tag Form'

    name = fields.Char('Tag Form')
    code = fields.Char('code')


class DataMaterial(models.Model):
    _name = 'data.material'
    _description = 'Material'

    name = fields.Char('Material')
    code = fields.Char('code')


class DataAplication(models.Model):
    _name = 'data.application.mode'
    _description = 'Aplication Mode'

    name = fields.Char('Application Mode')
    code = fields.Char('code')


class DataAplicationPosition(models.Model):
    _name = 'data.application.position'
    _description = 'Application Position'

    name = fields.Char('Aplication Position')
    code = fields.Char('code')


class PrintType(models.Model):
    _name = 'print.type'
    _description = 'Print Type'

    name = fields.Char('Print Type')
    code = fields.Char('code')


class ChemicalComposition(models.Model):
    _name = 'chemical.composition'
    _description = 'Chemical Composition'

    name = fields.Char('Chemical Composition')
    code = fields.Char('code')


class SpecificationWidth(models.Model):
    _name = 'specification.width'
    _description = 'Specification Width'

    name = fields.Float('Specification Width')
    code = fields.Char('code')
    tolerance = fields.Float('Tolerance')


class SpecificationLong(models.Model):
    _name = 'specification.long'
    _description = 'Specification Long'
    _rec_name = 'code'

    name = fields.Float('Specification Long')
    tolerance = fields.Float("Tolerance")
    room_large = fields.Char('Room Large')
    large_planned = fields.Float('Large Planned')
    code = fields.Char('code', compute='default_code')

    def default_code(self):
        for rec in self:
            if rec.name and rec.room_large:
                rec.code = str(rec.name) + '-' + str(rec.room_large)
            else:
                rec.code = ''


class WidthOverlap(models.Model):
    _name = 'width.overlap'
    _description = 'Width Overlap'

    name = fields.Float('Width Overlap')
    tolerance = fields.Char('Tolerance')
    code = fields.Char('code')


class OverlapLocation(models.Model):
    _name = 'overlap.location'
    _description = 'Overlap Location'

    name = fields.Char('Overlap Location')
    code = fields.Char('code')


class Presentation(models.Model):
    _name = 'presentation'
    _description = 'Presentation'

    name = fields.Char('Presentation')
    code = fields.Char('code')


class CoreDiameter(models.Model):
    _name = 'core.diameter'
    _description = 'Core Diameter'

    name = fields.Char('Core Diameter')
    code = fields.Char('code')


class EmbossingNumber(models.Model):
    _name = 'embossing.number'
    _description = 'Embossing Number'

    name = fields.Char('Embossing Number')
    code = fields.Char('code')


class NumberSplices(models.Model):
    _name = 'number.splices'
    _description = 'Number of splices'

    name = fields.Char('Number splices')
    code = fields.Char('code')


class SpliceType(models.Model):
    _name = 'splice.type'
    _description = 'Splice type'

    name = fields.Char('Splice type')
    code = fields.Char('code')


class SplicingTape(models.Model):
    _name = 'splicing.tape'
    _description = 'Splicing tape'

    name = fields.Char('Splicing tape')
    code = fields.Char('code')


class Seal_Type(models.Model):
    _name = 'seal.type'
    _description = 'Seal Type'

    name = fields.Char('Seal Type')
    seal = fields.Float('Seal')
    code = fields.Char('code')


class Preformed(models.Model):
    _name = 'preformed'
    _description = 'Preformed Table'

    name = fields.Char('Mold')
    bottom_diameter = fields.Float('Bottom Diameter')
    upper_diameter = fields.Float('Upper Diameter')
    tab_length = fields.Float('Tab Length')
    band_height = fields.Float('Band Height')
    product = fields.Char('Product')


class BarcodeType(models.Model):
    _name = 'barcode.type'
    _description = 'Barcode Type'

    name = fields.Char('Barcode Type')
    code = fields.Char('code')


class MechanicPlan(models.Model):
    _name = 'mechanic.plan'
    _description = 'Mechanic Plan'

    name = fields.Binary('Mechanic Plan')
    code = fields.Char('code')


class Microperforated(models.Model):
    _name = 'microperforated'
    _description = 'Microperforated'

    name = fields.Char('code')
    cross = fields.Char('Cross')
    logitudinal = fields.Char('Longitudinal')


class GraphitePresentation(models.Model):
    _name = 'drawn.presentation'
    _description = 'Drawn Presentation'

    name = fields.Char('Drawn Presentation')
    drawn_type = fields.Char('Drawn Type')
    code = fields.Char('code')


class AdhesiveType(models.Model):
    _name = 'adhesive.type'
    _description = 'Adhesive Type'

    name = fields.Char('Adhesive Type')
    code = fields.Char('code')


class ColdFoil(models.Model):
    _name = 'cold.foil'
    _description = 'Cold Foil'

    name = fields.Char('Cold Foil')
    code = fields.Char('code')


class Inks(models.Model):
    _name = 'inks'
    _description = 'Special Inks'

    name = fields.Selection([('barnizm', 'Barniz Mate'), ('barnizt', 'Barniz Textura'), ('plata', 'Plata Espejo'),
                             ('polvo', 'Polvo oro verdoso')], 'Ink')
    percentage = fields.Selection(
        [('5', '5'), ('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'), ('80', '80'),
         ('100', '100')], 'Percentage')


class Designer(models.Model):
    _name = 'designer'
    _description = 'Designer'

    name = fields.Char('Designer')
    code = fields.Char('code')
    zone = fields.Char('zone')


class ColorScale(models.Model):
    _name = 'color.scale'
    _description = 'Color scale'

    name = fields.Float('Color scale/check mark')


class ControlChange(models.Model):
    _name = 'control.change'
    _description = 'Control Change'

    name = fields.Char('Change')
    date = fields.Date('Date')
    vendor = fields.Many2one('res.partner', 'Vendor')


class Tape(models.Model):
    _name = 'tape'
    _description = 'Tape'

    name = fields.Char('tape')
    tape_to = fields.Date('Tape to')


class Rewind(models.Model):
    _name = 'rewind'
    _description = 'Rewind'

    name = fields.Char('Rewind')


"""class PrintColor(models.Model):
    _name = 'print.color'
    _description = 'Print Color'

    name = fields.Many2one('product.product','Color')
    press = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8')],'U.Press')
    percentage = fields.Selection([('5', '5'), ('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'),('80', '80'),('100', '100')], 'Percentage')
    line = fields.Selection([('bs','BS'),('ba', 'BA'),('uv','UV')],'Line')
    lineatura = fields.Char('Lineatura')
    bcm = fields.Char('BCM')"""


class Repeat(models.Model):
    _name = 'repeat'
    _description = 'Repeat'

    name = fields.Char('Roller', required=True)
    large_planned = fields.Many2one('specification.long', 'Large Planned', required=True)


class ForSuperlon(models.Model):
    _name = 'for.superlon'
    _description = 'For Superlon'

    name = fields.Char('For Superlon')


class MathPrint(models.Model):
    _name = 'match.print.line'
    _description = 'Match Print Line'

    match_print_id = fields.Many2one('data.sheet', 'Name')
    datetime = fields.Datetime('Date and Hour')
    quantity = fields.Char('Quantity')
    customer = fields.Many2one('res.partner', 'Customer')
    sign_vendor = fields.Binary('Sign Vendor')
    deliver_to = fields.Many2one('res.partner', 'Deliver to')
    sign_designer = fields.Binary('Sign Designer')
    vendor_date = fields.Date('Application date vendor')
    date_recieved_approved = fields.Date('Date Recieved Approved')
    observations = fields.Char('Observations')


class DrawnPass(models.Model):
    _name = 'drawn.pass'
    _description = 'Drawn Pass'

    name = fields.Char('Drawn Pass')
    code = fields.Char('Code')

class PantonePrint(models.Model):
    _name = 'pantone.print'
    _description = 'Pantone Print'

    name = fields.Char('Pantone')
    code = fields.Char('Code')
    color_ids = fields.One2many('data.sheet.line','pantone_id','Colors')