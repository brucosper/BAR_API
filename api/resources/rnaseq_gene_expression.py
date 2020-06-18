import re
from flask_restful import Resource
from api.models.single_cell import SingleCell
from api.utilities.bar_utilites import BARUtilities


class RNASeqGeneExpression(Resource):
    def get(self, species='', database='', gene_id='', sample_id=''):
        """
        This function returns a Gene Expression Value an AGI ID.

        :param species: Common name of species
        :param database: Database name
        :param gene_id: AGI ID
        :param sample_id: Sample id
        :return: json Gene alias object
        """

        result = {}
        data = None

        # Output help
        if species == 'species' or species is None or species == '':
            return BARUtilities.success_exit(['arabidopsis'])

        if database == 'databases' or database is None or database == '':
            return BARUtilities.success_exit(['single_cell'])

        # Set model
        if database == 'single_cell':
            database = SingleCell()
        else:
            BARUtilities.error_exit('Invalid database')

        # Validate data
        if species == 'arabidopsis':
            if not re.search(r"^At[12345CM]g\d{5}$", gene_id, re.I):
                return BARUtilities.success_exit('Invalid gene id')

        if not re.search(r"^[\D\d_\.]{0,40}$", sample_id):
            return BARUtilities.error_exit('Invalid sample id')

        # Now query the database
        if sample_id == '' or sample_id is None:
            rows = database.query.filter_by(data_probeset_id=gene_id).all()
        else:
            rows = database.query.filter_by(data_probeset_id=gene_id, data_bot_id=sample_id).all()

        data = {}
        for row in rows:
            data[row.data_bot_id] = row.data_signal

        # Return results if there are data
        if len(data) > 0:
            result['status'] = 'success'
            result['data'] = data
        else:
            return BARUtilities.error_exit('There is no data found for the given gene')

        return result