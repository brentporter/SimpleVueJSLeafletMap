<template>
    <div id="mapTexas"></div>
</template>

<script>
    import L from "leaflet";
    import * as esri from "esri-leaflet";
    import * as wmts from 'leaflet-tilelayer-wmts';
    //import * as dates from './scripts/txCapDatesParsing';
    // import * as sorties from './scripts/sortieParsing';
    // the following three imports are from sortieParsing to fold in the TxCap Processing
    import axios from 'axios';
    import * as MakiMarkers from './scripts/Leaflet.MakiMarkers';
    import './scripts/utility';
    //import '../'

    let movesMap;
    let esriAerialsLayer;
    let esriAerialsLabels;
    let esriToposLayer;
    let esriStreetsLayer;
    let googleImageryLayer;
    let geoJsonQPF_Day1;
    let geoJsonQPF_Day2;
    let collectDateQuery;
    let testBBox;
    let geoJsonSorties;
    let maskingSentinelApr16;
    window.retrieveNextPhoto = retrieveNextPhoto;
    window.retrieveNextPhotoKeyboards = retrieveNextPhotoKeyboards;

    /*
        let esriAerialsLayer;
        let esriAerialsLabels;
        let esriToposLayer;
        let esriStreetsLayer;
        let geoJsonQPF_Day1;
        let geoJsonQPF_Day2;
    */

    export default {
        name: "Map",
        data() {
            return {
                map: [],
                markers: null,
                txCapQueryTotalRecordsCount:null,
                txCapQueryCurrentDate:null,
                txCapQuerySpatial:null,
            }
        },
        methods:{
            //initializeMap: initializeMap()
            toggleLayer: toggleLayer,
            addRemoveGauges:addRemoveGauges,
            addRemoveMaskTornado:addRemoveMaskTornado,
            handleAddForecast1DayLayer,
            handleAddForecast2DayLayer,
            addRemoveSensorLayer,
            changeSensorImgOpacity,
            resetMap,
            redrawMap,
            goToBookmark,
            goToLocation,
            getMapInfo,
            clearTxCapPhotoTour,
            retrieveTxCap,
            retrieveTxCapCount:retrieveTxCapCount,
            sortieCountEnvelopeFirst,
            sortieCountEnvelope,
            handleDatesFetching:handleDatesFetching,
            reallyIGotThis:reallyIGotThis,
        },
        mounted(){
            //console.log(this.$store.state.count);
            esriToposLayer = esri.basemapLayer("Topographic");
            esriAerialsLayer = esri.basemapLayer('Imagery',{attribution: "ESRI et al",hideLogo:"true"});
            esriAerialsLabels = esri.basemapLayer('ImageryLabels');
            esriStreetsLayer = esri.basemapLayer('Streets',{attribution: "ESRI et al",hideLogo:"true"});
            googleImageryLayer = wmts.tileLayerWMTS('https://txgi.tnris.org/login/path/arena-baker-mouse-bonus/wmts?' ,
                {
                    layer: 'texas',
                    style: "normal",
                    tilematrixSet: "0to20",
                    maxZoom: 20,
                    transparent: true,
                    format: "image/png"
                }
            );
            movesMap = L.map("mapTexas", {
                center: [32.3117, -99.77774],
                zoom: 6,
                layers: [
                    esriToposLayer
                    /* L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
                         attribution:
                             '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                     })*/

                ]
            });
            geoJsonQPF_Day1 = L.geoJson(qpfDay1,
                {
                    style: function(feature) {
                        switch (feature.properties.QPF) {
                            //case '723-011': return {color: "#ff0000"};
                            //case '723-071': return {color: "#ff0000"};
                            //case '723-075': return {color: "#ff0000"};
                            //case '723-121': return {color: "#ff0000"};
                            //case '723-049': return {color: "#ff0000"};
                            case 0.010000: return {color: "#79FA00",fillOpacity:0.45,weight: 0.2};
                            case 0.100000: return {color: "#00CF00",fillOpacity:0.45,weight: 0.2};
                            case 0.250000: return {color: "#008C00",fillOpacity:0.45,weight: 0.2};
                            case 0.500000: return {color: "#114B8D",fillOpacity:0.45,weight: 0.2};
                            case 0.750000: return {color: "#1E90FF",fillOpacity:0.45,weight: 0.2};
                            case 1.000000: return {color: "#00B2EE",fillOpacity:0.45,weight: 0.2};
                            case 1.250000: return {color: "#00EEEE",fillOpacity:0.45,weight: 0.2};
                            case 1.500000: return {color: "#8967CC",fillOpacity:0.45,weight: 0.2};
                            case 1.750000: return {color: "#9133EE",fillOpacity:0.45,weight: 0.2};
                            case 2.000000: return {color: "#8B1E8B",fillOpacity:0.45,weight: 0.2};
                            case 2.500000: return {color: "#8A0F00",fillOpacity:0.45,weight: 0.2};
                            case 3.000000: return {color: "#CE1C00",fillOpacity:0.45,weight: 0.2};
                            case 4.000000: return {color: "#ED4000",fillOpacity:0.45,weight: 0.2};
                            case 5.000000: return {color: "#FF7F00",fillOpacity:0.45,weight: 0.2};
                            case 7.000000: return {color: "#CE8500",fillOpacity:0.45,weight: 0.2};
                            case 10.000000: return {color: "#FFD700",fillOpacity:0.45,weight: 0.2};
                            case 15.000000: return {color: "#FFFB00",fillOpacity:0.45,weight: 0.2};
                            case 20.000000: return {color: "#FFAEB8",fillOpacity:0.45,weight: 0.2};
                            default:
                                return {color: '#00008A'};
                            //break;
                        }
                    }

                });

            geoJsonQPF_Day2 = L.geoJson(qpfDay2,
                {
                    style: function(feature) {
                        switch (feature.properties.QPF) {
                            //case '723-011': return {color: "#ff0000"};
                            //case '723-071': return {color: "#ff0000"};
                            //case '723-075': return {color: "#ff0000"};
                            //case '723-121': return {color: "#ff0000"};
                            //case '723-049': return {color: "#ff0000"};
                            case 0.010000: return {color: "#79FA00",fillOpacity:0.45,weight: 0.2};
                            case 0.100000: return {color: "#00CF00",fillOpacity:0.45,weight: 0.2};
                            case 0.250000: return {color: "#008C00",fillOpacity:0.45,weight: 0.2};
                            case 0.500000: return {color: "#114B8D",fillOpacity:0.45,weight: 0.2};
                            case 0.750000: return {color: "#1E90FF",fillOpacity:0.45,weight: 0.2};
                            case 1.000000: return {color: "#00B2EE",fillOpacity:0.45,weight: 0.2};
                            case 1.250000: return {color: "#00EEEE",fillOpacity:0.45,weight: 0.2};
                            case 1.500000: return {color: "#8967CC",fillOpacity:0.45,weight: 0.2};
                            case 1.750000: return {color: "#9133EE",fillOpacity:0.45,weight: 0.2};
                            case 2.000000: return {color: "#8B1E8B",fillOpacity:0.45,weight: 0.2};
                            case 2.500000: return {color: "#8A0F00",fillOpacity:0.45,weight: 0.2};
                            case 3.000000: return {color: "#CE1C00",fillOpacity:0.45,weight: 0.2};
                            case 4.000000: return {color: "#ED4000",fillOpacity:0.45,weight: 0.2};
                            case 5.000000: return {color: "#FF7F00",fillOpacity:0.45,weight: 0.2};
                            case 7.000000: return {color: "#CE8500",fillOpacity:0.45,weight: 0.2};
                            case 10.000000: return {color: "#FFD700",fillOpacity:0.45,weight: 0.2};
                            case 15.000000: return {color: "#FFFB00",fillOpacity:0.45,weight: 0.2};
                            case 20.000000: return {color: "#FFAEB8",fillOpacity:0.45,weight: 0.2};
                            default:
                                return {color: '#00008A'};
                            //break;
                        }
                    }

                });

            let lineTornado = turf.lineString([[-95.402527,31.264172],[-95.39566,31.299382],[-95.354462,31.32754],[-95.333862,31.354517],[-95.310516,31.386175],
                [-95.292664,31.407275],[-95.266571,31.429542],[-95.248718,31.455318],[-95.225372,31.488114],[-95.204773,31.517386],[-95.19516,31.527922],
                [-95.185547,31.540797],[-95.175934,31.554841],[-95.169067,31.573563],[-95.159454,31.586432],[-95.145721,31.60046],[-95.126495,31.613335],
                [-95.111389,31.633214],[-95.09491,31.649582],[-95.081177,31.662441],[-95.059204,31.678804],[-95.044098,31.688153],[-95.026245,31.703343],
                [-95.011139,31.71853],[-94.991913,31.727875],[-94.976807,31.745394],[-94.964447,31.760575]],{name:'Alto Callout Track'});
            let polyFootprint = turf.polygon([[[-95.767822, 32.109333],[-93.169556, 32.503971],[-92.872925, 31.023517],[-95.443726, 30.63673],[-95.767822, 32.109333]]],{name:'Sentinel 1 Footprint'});
            //[-95.8122343032567,30.6096779992903],[-92.8304563806788,32.5241675328058]
            let bbox = turf.bbox(polyFootprint);
            let bufferedTornadoTrack = turf.buffer(lineTornado,3,{units:'miles'});
            console.log(bufferedTornadoTrack);

            let maskedTrack = turf.mask(bufferedTornadoTrack,polyFootprint,{name:'Alto Mask'});
            maskedTrack.properties.name = 'Alto Mask';
            maskingSentinelApr16 = L.geoJSON(maskedTrack, {
                style: function (feature) {
                    return {
                        color: 'grey',
                        opacity: 1,
                        fillOpacity:0.8,
                    };
                }
            }).bindPopup(function (layer) {
                return layer.feature.properties.name;
            });
            //noaaPortAransas20170829a
            //addRemoveSensorLayer('noaaDMC','noaaPortAransas20170829a');
            //addRemoveGauges('forecastGauges');
            //addRemoveGauges('gauges');
            //this.handleDatesFetching('default');
        },
        created(){
            //Menu Components used to pass over Global Event hub these events from buttons
            this.$eventHub.$on('toggleMapLayers', this.toggleLayer);
            this.$eventHub.$on('toggleGaugesLayers', this.addRemoveGauges);
            this.$eventHub.$on('handleAddForecast1DayLayer',this.handleAddForecast1DayLayer);
            this.$eventHub.$on('handleAddForecast2DayLayer',this.handleAddForecast2DayLayer);
            this.$eventHub.$on('toggleSensorLayer', this.addRemoveSensorLayer);
            this.$eventHub.$on('changeOpacityImagery',this.changeSensorImgOpacity);
            this.$eventHub.$on('resetMap',this.resetMap);
            this.$eventHub.$on('goToBookmarks',this.goToBookmark);
            this.$eventHub.$on('goToLocation',this.goToLocation);
            //this.$eventHub.$on('goToLocation',this.goToNamedLocation);
            this.$eventHub.$on('gatheringMapInfo',this.getMapInfo);
            this.$eventHub.$on('redrawMap',this.redrawMap);
            this.$eventHub.$on('retrieveTxCapByDateCount',this.retrieveTxCapCount);
            this.$eventHub.$on('retrieveTxCapByDate',this.retrieveTxCap);
            this.$eventHub.$on('retrieveTxCapByEnvelopeCount',this.sortieCountEnvelopeFirst);
            this.$eventHub.$on('retrieveTxCapByEnvelope',this.sortieCountEnvelope);
            this.$eventHub.$on('clearTxCapEnvelope',this.clearTxCapPhotoTour);
            //toggleMaskTornado20190416
            this.$eventHub.$on('toggleMaskTornado20190416', this.addRemoveMaskTornado);
        }
    }

/*    function txCapProcessing(incomingDateStr){
        //console.log(movesMap);
        sorties.retrieveTxCap(incomingDateStr,movesMap);
    }*/

/*    function retrieveNextPhoto(incomingImageId,incrementor){
        console.log("Inside retrieve next photo");
        sorties.retrieveNextPhoto(incomingImageId,incrementor)
    }*/

    function resetMap(){
        /*if(!movesMap.hasLayer(esriToposLayer)){
            movesMap.addLayer(esriToposLayer);
            checkRemoveAerials();
            checkRemoveStreets();
            checkRemoveGoogleWMTS();
        }*/
        movesMap.setView([32.3117, -99.77774], 6);
        movesMap.invalidateSize();
    }

    function redrawMap(){
        console.log('Here');
        movesMap.invalidateSize();
        //movesMap.redraw();
    }

    function getMapInfo(){
        /*if(!movesMap.hasLayer(esriToposLayer)){
            movesMap.addLayer(esriToposLayer);
            checkRemoveAerials();
            checkRemoveStreets();
            checkRemoveGoogleWMTS();
        }*/
        //movesMap.getZoom();
        //movesMap.getCenter();
        const LatLngAry = [movesMap.getCenter().lat,movesMap.getCenter().lng];
        let mapInfoObj = {ZoomLevel:movesMap.getZoom(),LatLng:LatLngAry};
        //movesMap.setView([32.3117, -99.77774], 6);
        //TODO:Convert to Vuex BAP 04-03-19
        this.$eventHub.$emit('returnedMapInfo',mapInfoObj);
    }

    function addRemoveMaskTornado(){
        if(movesMap.hasLayer(maskingSentinelApr16)){
            movesMap.removeLayer(maskingSentinelApr16);
        } else {
            movesMap.addLayer(maskingSentinelApr16);
        }
    }

    function handleDatesFetching(incomingChoice) {
        let eventDates = '';
        if(incomingChoice==='default'){
            //if(!incomingMap.hasLayer(geoJsonCurrentGauges)) {// use false for turning on - true for turning off
            let urlFetch = 'http://129.116.70.166/ida_txcap/api/txCap/dates/availableDates/1';
            axios.get(urlFetch)
                .then(response=>{
                    //return response.data
                    console.log(response.data);
                    eventDates = response.data;
                    if(eventDates!==''){
                        this.reallyIGotThis(eventDates);
                    }
                })
                .catch(error=>{
                    console.log(error);
                });
            //} else {
            //incomingMap.removeLayer(geoJsonCurrentGauges);
            //}
        }
    }

    function reallyIGotThis(incomingEventsDate){
        //this.$eventHub.$emit('returnedMapInfo',mapInfoObj);
        this.$eventHub.$emit('initDates', incomingEventsDate);
    }

    function goToLocation(incomingObj){
        console.log("Go To Location");
        console.log(incomingObj);
        console.log(incomingObj.LatLng);
        const LatLngAry = [incomingObj.LatLng[0],incomingObj.LatLng[1]];
        console.log(LatLngAry);
        movesMap.setView(LatLngAry,incomingObj.ZoomLevel);
        movesMap.invalidateSize();
    }

    function goToBookmark(incomingBookmark){
        if(incomingBookmark==='seTx'){
            movesMap.setView([30.072659, -95.202026], 8);
        } else if (incomingBookmark==='southTx'){
            movesMap.setView([27.550894, -98.195801], 8);
        } else if (incomingBookmark==='ncTx'){
            movesMap.setView([32.78612, -97.047729], 8);
        } else if (incomingBookmark==='westTx'){
            movesMap.setView([30.721768, -103.447266], 8);
        } else if (incomingBookmark==='centralTx'){
            movesMap.setView([30.229408, -98.146362], 8);
        }
        movesMap.invalidateSize();
    }

    function toggleLayer(incomingLayer){
        //console.log(incomingLayer);
        //console.log(esriToposLayer);
        if (incomingLayer==='topo'){
            console.log(incomingLayer);
            if(!movesMap.hasLayer(esriToposLayer)){
                movesMap.addLayer(esriToposLayer);

            }
            checkRemoveAerials();
            checkRemoveStreets();
            checkRemoveGoogleWMTS();
        }
        else if(incomingLayer==='aerials'){
            if(movesMap.hasLayer(esriAerialsLayer)){
                if(!movesMap.hasLayer(esriToposLayer)){
                    movesMap.addLayer(esriToposLayer);
                }
                checkRemoveStreets();
                checkRemoveAerials();
                checkRemoveGoogleWMTS();
            }
            else {
                checkRemoveGoogleWMTS();
                movesMap.addLayer(esriAerialsLayer);
                movesMap.addLayer(esriAerialsLabels);
                checkRemoveTopo();
                checkRemoveStreets();
            }
        } else if(incomingLayer==='streets'){
            if(movesMap.hasLayer(esriStreetsLayer)){
                if(!movesMap.hasLayer(esriToposLayer)){
                    movesMap.addLayer(esriToposLayer);
                }
                checkRemoveStreets();
                checkRemoveGoogleWMTS();
                checkRemoveAerials();
            }
            else {
                movesMap.addLayer(esriStreetsLayer);
                checkRemoveGoogleWMTS();
                checkRemoveTopo();
                checkRemoveAerials();
            }
        } else if(incomingLayer==='reset'){
            //console.log('Reset');
            if(!movesMap.hasLayer(esriToposLayer)){
                movesMap.addLayer(esriToposLayer);
                checkRemoveAerials();
                checkRemoveStreets();
                checkRemoveGoogleWMTS();
            }
            movesMap.setView([32.3117, -99.77774], 6);
        }  else if(incomingLayer==='google'){
            if(movesMap.hasLayer(googleImageryLayer)){
                movesMap.removeLayer(googleImageryLayer);
                checkRemoveLabelsOnly();
                checkRemoveAerials();
                if(!movesMap.hasLayer(esriToposLayer)){
                    movesMap.addLayer(esriToposLayer);
                }
                //console.log("Am I here?");
            } else {
                if(!movesMap.hasLayer(esriToposLayer)){
                    movesMap.addLayer(esriToposLayer);
                }
                movesMap.addLayer(googleImageryLayer);
                checkRemoveAerials();
                checkRemoveStreets();
                if(!movesMap.hasLayer(esriAerialsLabels))
                {
                    movesMap.addLayer(esriAerialsLabels);
                    //movesMap.bringToFront(esriAerialsLabels);
                }
            }
        }

    }

    function checkRemoveLabelsOnly(){
        if(movesMap.hasLayer(esriAerialsLabels)){
            movesMap.removeLayer(esriAerialsLabels);
        }
    }

    function checkRemoveAerials(){
        if(movesMap.hasLayer(esriAerialsLayer)){
            movesMap.removeLayer(esriAerialsLayer);
            movesMap.removeLayer(esriAerialsLabels);
        }
    }

    function checkRemoveStreets(){
        if(movesMap.hasLayer(esriStreetsLayer)){
            movesMap.removeLayer(esriStreetsLayer);
        }
    }

    function checkRemoveTopo(){
        if(movesMap.hasLayer(esriToposLayer)) {
            movesMap.removeLayer(esriToposLayer);
        }
    }

    function checkRemoveGoogleWMTS(){
        if(movesMap.hasLayer(googleImageryLayer)){
            movesMap.removeLayer(googleImageryLayer);
        }
        checkRemoveLabelsOnly();
    }

    function addRemoveGauges(incomingGaugesLayer) {
        //console.log("Here");
        gauges.handleFetching(incomingGaugesLayer,movesMap);
    }

    function handleAddForecast1DayLayer(){
        if(movesMap.hasLayer(geoJsonQPF_Day1)){
            movesMap.removeLayer(geoJsonQPF_Day1);
        } else {
            movesMap.addLayer(geoJsonQPF_Day1);
            if(movesMap.hasLayer(geoJsonQPF_Day2)){
                movesMap.removeLayer(geoJsonQPF_Day2);
            }
        }
    }

    function handleAddForecast2DayLayer(){
        if(movesMap.hasLayer(geoJsonQPF_Day2)){
            movesMap.removeLayer(geoJsonQPF_Day2);
        } else {
            movesMap.addLayer(geoJsonQPF_Day2);
            if(movesMap.hasLayer(geoJsonQPF_Day1)){
                movesMap.removeLayer(geoJsonQPF_Day1);
            }
        }
    }

    function changeSensorImgOpacity(incomingSensorType,incomingSensorOpacity,incomingSensorDateName){
        if(incomingSensorType==='spotSensor'){
            console.log("Here Yep!!!");
            if (sensors.sensorLayerObj.spotSensor.findIndex(x => x.name === incomingSensorDateName) !== -1) {
                console.log("Now I am here");
                let idxSensor = sensors.sensorLayerObj.spotSensor.findIndex(x => x.name === incomingSensorDateName);
                let sensorCalled = sensors.sensorLayerObj.spotSensor[idxSensor];
                if (movesMap.hasLayer(sensorCalled.layer)) {
                    sensorCalled.layer.setOpacity(incomingSensorOpacity/100);
                }
            }
        }

    }

    function addRemoveSensorLayer(incomingSensorType,incomingSensorDateName){
        console.log("What up????");
        if(incomingSensorType==='noaaDMC') {
            if (sensors.sensorLayerObj.noaaDMC.findIndex(x => x.name === incomingSensorDateName) !== -1) {
                let idxSensor = sensors.sensorLayerObj.noaaDMC.findIndex(x => x.name === incomingSensorDateName);
                let sensorCalled = sensors.sensorLayerObj.noaaDMC[idxSensor];
                //console.log(movesMap.getBounds());
                let cornerNE = L.latLng(sensorCalled.northeast[0],sensorCalled.northeast[1]);
                let cornerSW = L.latLng(sensorCalled.southwest[0],sensorCalled.southwest[1]);
                let sensorView = L.latLng(sensorCalled.view[0],sensorCalled.view[1]);
                let boundsSensor = L.latLngBounds(cornerNE,cornerSW);
                //console.log(sensorCalled.zoom);
                //console.log("bellweather");
                if (movesMap.hasLayer(sensorCalled.layer)) {
                    movesMap.removeLayer(sensorCalled.layer);
                } else {
                    movesMap.addLayer(sensorCalled.layer);
                    if(movesMap.getZoom()<=sensorCalled.zoom) {
                        movesMap.setView(sensorView, sensorCalled.zoom);
                    }
                    /*if(movesMap.getZoom()>=sensorCalled.zoom) {
                        movesMap.setView(sensorView, movesMap.getZoom());
                    } else {
                        movesMap.setView(sensorView, sensorCalled.zoom);
                    }*/
                }
            }
        } else if(incomingSensorType==='isroAWIFS'){
            if (sensors.sensorLayerObj.isroAWIFS.findIndex(x => x.name === incomingSensorDateName) !== -1) {
                console.log('Inside name index check');
                let idxSensor = sensors.sensorLayerObj.isroAWIFS.findIndex(x => x.name === incomingSensorDateName);
                let sensorCalled = sensors.sensorLayerObj.isroAWIFS[idxSensor];
                let cornerNE = L.latLng(sensorCalled.northeast[0],sensorCalled.northeast[1]);
                let cornerSW = L.latLng(sensorCalled.southwest[0],sensorCalled.southwest[1]);
                let sensorView = L.latLng(sensorCalled.view[0],sensorCalled.view[1]);
                let boundsSensor = L.latLngBounds(cornerNE,cornerSW);
                //console.log(sensorCalled.zoom);
                //console.log("bellweather");
                if (movesMap.hasLayer(sensorCalled.layer)) {
                    movesMap.removeLayer(sensorCalled.layer);
                } else {
                    movesMap.addLayer(sensorCalled.layer);
                    if(movesMap.getZoom()>=sensorCalled.zoom) {
                        movesMap.setView(sensorView, movesMap.getZoom());
                    } else {
                        movesMap.setView(sensorView, sensorCalled.zoom);
                    }
                }
            }
        } else if(incomingSensorType==='sentinelSensor'){
            if (sensors.sensorLayerObj.sentinelSensor.findIndex(x => x.name === incomingSensorDateName) !== -1) {
                console.log('Inside name index check');
                let idxSensor = sensors.sensorLayerObj.sentinelSensor.findIndex(x => x.name === incomingSensorDateName);
                let sensorCalled = sensors.sensorLayerObj.sentinelSensor[idxSensor];
                let cornerNE = L.latLng(sensorCalled.northeast[0],sensorCalled.northeast[1]);
                let cornerSW = L.latLng(sensorCalled.southwest[0],sensorCalled.southwest[1]);
                let sensorView = L.latLng(sensorCalled.view[0],sensorCalled.view[1]);

                ///let maskingSentinelApr16='';
                let boundsSensor = L.latLngBounds(cornerNE,cornerSW);
                //console.log(sensorCalled.zoom);
                //console.log("bellweather");
                if (movesMap.hasLayer(sensorCalled.layer)) {
                    movesMap.removeLayer(sensorCalled.layer);
                    //console.log("Here " + movesMap.hasLayer(maskingSentinelApr16));
                    if(movesMap.hasLayer(maskingSentinelApr16)) {
                        movesMap.removeLayer(maskingSentinelApr16);
                    }
                } else {
                    movesMap.addLayer(sensorCalled.layer);
                    if(movesMap.getZoom()>=sensorCalled.zoom) {
                        //movesMap.setView(sensorView, movesMap.getZoom());
                    } else {
                        movesMap.setView(sensorView, sensorCalled.zoom);
                    }

                    //movesMap.addLayer(maskingSentinelApr16);

                }
            }
        } else if(incomingSensorType==='spotSensor'){
            if (sensors.sensorLayerObj.spotSensor.findIndex(x => x.name === incomingSensorDateName) !== -1) {
                let idxSensor = sensors.sensorLayerObj.spotSensor.findIndex(x => x.name === incomingSensorDateName);
                let sensorCalled = sensors.sensorLayerObj.spotSensor[idxSensor];
                let cornerNE = L.latLng(sensorCalled.northeast[0],sensorCalled.northeast[1]);
                let cornerSW = L.latLng(sensorCalled.southwest[0],sensorCalled.southwest[1]);
                let sensorView = L.latLng(sensorCalled.view[0],sensorCalled.view[1]);
                let boundsSensor = L.latLngBounds(cornerNE,cornerSW);
                //console.log(sensorCalled.zoom);
                //console.log("bellweather");
                if (movesMap.hasLayer(sensorCalled.layer)) {
                    movesMap.removeLayer(sensorCalled.layer);
                } else {
                    movesMap.addLayer(sensorCalled.layer);
                    if(movesMap.getZoom()<=sensorCalled.zoom) {
                        movesMap.setView(sensorView, sensorCalled.zoom);
                    }
                    /*if(movesMap.getZoom()>=sensorCalled.zoom) {
                        movesMap.setView(sensorView, movesMap.getZoom());
                    } else {
                        movesMap.setView(sensorView, sensorCalled.zoom);
                    }*/
                }
            }
        }
    }

    function retrieveTxCapCount(incomingDate){//incomingDate
        //let queryString = 'http://129.116.70.166/ida_txcap/api/txCap/2018-10-23/';
        this.clearTxCapPhotoTour();
        let queryString = 'http://129.116.70.166/ida_txcap/api/txCap/'+incomingDate;
        //http://129.116.70.166/ida_txcap/api/txCap/2018-10-23/
        //this.$eventHub.$on('incomingTxCapCalendarQueryCounts',this.initializeTxCapCalendarPagination);
        axios.get(queryString)
            .then(response=>{
                //return response.data
                //handleGauges(response.data,incomingMap)
                //collectDateQuery = response.data.features[0].properties.collect_date;
                //console.log(response.data);
                //console.log(collectDateQuery);
                console.log("I am right before the count of records");
                console.log(response.data.features[0].properties.count_of_records);
                //sortiesLayerFunc(response.data);
                try {
                    let countReturnedRecords = parseInt(response.data.features[0].properties.count_of_records);
                    if (!isNaN(countReturnedRecords) && countReturnedRecords!==0) {
                        this.txCapQueryTotalRecordsCount = countReturnedRecords;
                        this.txCapQueryCurrentDate = incomingDate;
                        this.$eventHub.$emit('incomingTxCapCalendarQueryCounts', this.txCapQueryTotalRecordsCount,this.txCapQueryCurrentDate);
                    }
                } catch(exception){
                    console.log(exception.toString())
                }
            })
            .catch(error=>{
                console.log(error);
            });
    }

    function retrieveTxCap(incomingStartRecord){
        //this.clearTxCapPhotoTour();
        testBBox = movesMap.getBounds().toBBoxString().replace(/,/g,'/');
        let recordCountDateQuery = incomingStartRecord*500;
        if(this.txCapQueryTotalRecordsCount < recordCountDateQuery){
            recordCountDateQuery = this.txCapQueryTotalRecordsCount;
        }
        let adjPageNumber = incomingStartRecord-1;
        let startRecord = adjPageNumber*500;
        //http://129.116.70.166/ida_txcap/api/txCap/envelope/offset/-97.730743/30.926077/-93.619164/34.965345/0
        let queryString = "http://129.116.70.166/ida_txcap/api/txCap/dates/"+this.txCapQueryCurrentDate+"/"+recordCountDateQuery+"/" +startRecord;

        //console.log(incomingDate);
        //let urlFetch = 'http://magic.csr.utexas.edu/moves/public/views/txCap/' + incomingDate;
        //let urlFetch = queryString;
        axios.get(queryString)
            .then(response=>{
                //return response.data
                //handleGauges(response.data,incomingMap)
                collectDateQuery = response.data.features[0].properties.Collect_Date;
                //console.log(response.data);
                //console.log(collectDateQuery);
                sortiesLayerFunc(response.data);
            })
            .catch(error=>{
                console.log(queryString);
                console.log(error);
            });
    }

    function retrieveNextPhoto(incomingId,nextOrPrevious,incomingPhotoNumber,incomingImgPosition){
        if(nextOrPrevious === 'increment'){
            let nextIndicatorId = "#PhotoID" + incomingPhotoNumber;
            if(incomingImgPosition==='last') {
                if (!$('#finalIndicatorMsg').is(":visible")) {
                    sortiesMarkerPopup(nextIndicatorId);
                    $(nextIndicatorId).siblings('#finalIndicatorMsg').toggle();
                    $(nextIndicatorId).toggle();
                }
            } else if(incomingImgPosition==='body'){
                sortiesMarkerPopup(nextIndicatorId);
            }
        }
        else if(nextOrPrevious === 'decrement'){
            let prevIndicatorId = "#PhotoID" + incomingPhotoNumber;
            if(incomingImgPosition==='first') {
                prevIndicatorId = prevIndicatorId + 'First';
                if(!$('#finalIndicatorFirstMsg').is(":visible")){
                    sortiesMarkerPopup(prevIndicatorId);
                    $(prevIndicatorId).siblings("#finalIndicatorFirstMsg").toggle();
                    $(prevIndicatorId).toggle();
                }
            } else if(incomingImgPosition==='body'){
                sortiesMarkerPopup(prevIndicatorId);
            }
        }
    }

    //Changing this for New JSON Calls to TxCap... 04/01/2019
    function retrieveNextPhotoRetooled(incomingId,nextOrPrevious,incomingNextPhotoNumber,incomingImgPosition){
        /*
        let recreatedSortie = incomingId.substring(0,incomingId.lastIndexOf("_")-1);
        console.log("PhotoID" + incomingId.substring(incomingId.lastIndexOf("_")+1,incomingId.length-4));
        let finalNextBeforeIndicatorId = "#PhotoID" + incomingId.substring(incomingId.lastIndexOf("_")+1,incomingId.length-4);
        //finalIndicatorFirstMsg
        let firstNextBeforeIndicatorId = "#PhotoID" + incomingId.substring(incomingId.lastIndexOf("_")+1,incomingId.length-4) + "First";

        */
        //sortiesMarkerPopup(incomingNextPhotoNumber);
        if(nextOrPrevious === 'increment' && incomingImgPosition==="first") {
            //console.log(obj.photoNameArray[obj.photoNameArray.indexOf(incomingId) + 1]);
            sortiesMarkerPopup(incomingNextPhotoNumber);
            //incomingId.substring(incomingId.lastIndexOf("_")+1,incomingId.length-4
            let firstPhotoId = "PhotoID"+obj.photoNameArray[0].substring(incomingId.lastIndexOf("_")+1,incomingId.length-4);
            //  UNCHECK THIS ONE FOR DEBUG console.log(firstPhotoId);
            if($('#finalIndicatorFirstMsg').is(":visible")){
                console.log("Is it true or false? " + $('#finalIndicatorFirstMsg').is(":visible"));
                $(firstNextBeforeIndicatorId).toggle();
                $('#finalIndicatorFirstMsg').toggle();
            }
        } else if(nextOrPrevious === 'decrement' && obj.photoNameArray.indexOf(incomingId) !== 0) {
            //console.log(obj.photoNameArray[obj.photoNameArray.indexOf(incomingId) - 1]);
            sortiesMarkerPopup(obj.photoNameArray[obj.photoNameArray.indexOf(incomingId) - 1]);
            let lastPhotoId = "PhotoID"+obj.photoNameArray[sortiePhotoNameAryLength-1].substring(incomingId.lastIndexOf("_")+1,incomingId.length-4);
            if($('#finalIndicatorMsg').is(":visible")){
                $(incomingNextPhotoNumber).toggle();
                $('#finalIndicatorMsg').toggle()
            }
        }

        let recreatedSortie = incomingId.substring(0,incomingId.lastIndexOf("_")-1);
        console.log("PhotoID" + incomingId.substring(incomingId.lastIndexOf("_")+1,incomingId.length-4));
        let finalNextBeforeIndicatorId = "#PhotoID" + incomingId.substring(incomingId.lastIndexOf("_")+1,incomingId.length-4);
        //finalIndicatorFirstMsg
        let firstNextBeforeIndicatorId = "#PhotoID" + incomingId.substring(incomingId.lastIndexOf("_")+1,incomingId.length-4) + "First";
        function reallyIHave2DoThis(incomingSortieName) {
            return $.map(sortieQueryMetaCollections, function (obj, index) {
                console.log(sortieQueryMetaCollections);
                //console.log(obj.sortieName);
                if (obj.sortieName === incomingSortieName) {
                    //console.log("I made it!");
                    let sortiePhotoNameAryLength = obj.photoNameArray.length;
                    //  UNCHECK THIS ONE FOR DEBUG console.log(obj.photoNameArray.indexOf(incomingId) + " " + sortiePhotoNameAryLength);
                    if(nextOrPrevious === 'increment' && obj.photoNameArray.indexOf(incomingId) !== sortiePhotoNameAryLength-1) {
                        //console.log(obj.photoNameArray[obj.photoNameArray.indexOf(incomingId) + 1]);
                        sortiesMarkerPopup(obj.photoNameArray[obj.photoNameArray.indexOf(incomingId) + 1]);
                        //incomingId.substring(incomingId.lastIndexOf("_")+1,incomingId.length-4
                        let firstPhotoId = "PhotoID"+obj.photoNameArray[0].substring(incomingId.lastIndexOf("_")+1,incomingId.length-4);
                        //  UNCHECK THIS ONE FOR DEBUG console.log(firstPhotoId);
                        if($('#finalIndicatorFirstMsg').is(":visible")){
                            console.log("Is it true or false? " + $('#finalIndicatorFirstMsg').is(":visible"));
                            $(firstNextBeforeIndicatorId).toggle();
                            $('#finalIndicatorFirstMsg').toggle()
                        }
                    } else if(nextOrPrevious === 'decrement' && obj.photoNameArray.indexOf(incomingId) !== 0) {
                        //console.log(obj.photoNameArray[obj.photoNameArray.indexOf(incomingId) - 1]);
                        sortiesMarkerPopup(obj.photoNameArray[obj.photoNameArray.indexOf(incomingId) - 1]);
                        let lastPhotoId = "PhotoID"+obj.photoNameArray[sortiePhotoNameAryLength-1].substring(incomingId.lastIndexOf("_")+1,incomingId.length-4);
                        if($('#finalIndicatorMsg').is(":visible")){
                            $(finalNextBeforeIndicatorId).toggle();
                            $('#finalIndicatorMsg').toggle()
                        }
                    } else if(obj.photoNameArray.indexOf(incomingId) === sortiePhotoNameAryLength-1){
                        //console.log("Last Image");
                        $(finalNextBeforeIndicatorId).toggle();
                        $('#finalIndicatorMsg').toggle();
                    } else if(obj.photoNameArray.indexOf(incomingId) === 0){
                        //console.log("First Image");
                        $(firstNextBeforeIndicatorId).toggle();
                        $('#finalIndicatorFirstMsg').toggle();
                    }
                    return obj;
                }

            });
        }
        let indexForReals = reallyIHave2DoThis(recreatedSortie);
        //console.log(indexForReals);
    }

    function retrieveNextPhotoKeyboards(incomingId,nextOrPrevious,event){
        switch (event.key) {
            case "ArrowLeft":
                // Left pressed
                console.log("Left!");
                break;
            case "ArrowRight":
                // Right pressed
                console.log("Right!");
                break;
            case "ArrowUp":
                // Up pressed
                break;
            case "ArrowDown":
                // Down pressed
                break;
        }

    }

    function firstSortiePhoto(incomingImgPosition,incomingPhotoNumber){
        if(incomingImgPosition ==='body' || incomingImgPosition === 'last'){
            return 'font-weight: bold;display:none;padding-right:10px';
        } else if(incomingImgPosition === 'first'){
            let existingIndicatorId = "#PhotoID" + incomingPhotoNumber + "First";
            $(existingIndicatorId).toggle();
            return 'font-weight: bold;display:block;padding-right:10px';
        }
        return null;
    }

    function lastSortiePhoto(incomingImgPosition,incomingPhotoNumber){
        if(incomingImgPosition ==='body' || incomingImgPosition === 'first'){
            return 'font-weight: bold;display:none;padding-right:10px';
        } else if(incomingImgPosition === 'last'){
            let existingIndicatorId = "#PhotoID" + incomingPhotoNumber;
            $(existingIndicatorId).toggle();
            return 'font-weight: bold;display:block;padding-right:10px';
        }
        return null;
    }

    function sortiesLayerFunc(incomingData){
        //console.log(incomingData.features[0].properties.class);
        console.log(incomingData);
        if(movesMap.hasLayer(geoJsonSorties)){
            movesMap.removeLayer(geoJsonSorties);
        }
        //MakiMarkers.default.
        geoJsonSorties = L.geoJson(incomingData,
            {
                pointToLayer: function (feature, latlng) {
                    let surveyedCo_Marker;
                    if(feature.properties.Name.indexOf("DPS")!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "heliport",
                            color: "#ffb900",
                            size: "m"
                        });
                    } //For Oct 21, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1021Z0001')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#ffa433",
                            size: "m"
                        });
                    } //For Oct 21, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1021Z0002')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#cc25a6",
                            size: "m"
                        });
                    } //For Oct 21, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1021Z0003')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#1c47aa",
                            size: "m"
                        });
                    } //For Oct 21, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1021Z0004')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#17aa7c",
                            size: "m"
                        });
                    } //For Oct 22, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1022A0027')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#ffb900",
                            size: "m"
                        });
                    } //For Oct 22, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1022A0033')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#c24ecc",
                            size: "m"
                        });
                    } //For Oct 22, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1022A0035')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#089faa",
                            size: "m"
                        });
                    } //For Oct 23, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1023Z0001')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#aa6a22",
                            size: "m"
                        });
                    } //For Oct 23, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1023Z0002')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#6caa89",
                            size: "m"
                        });
                    } //For Oct 23, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1023Z0003')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#4a42aa",
                            size: "m"
                        });
                    } //For Oct 23, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1023Z0004')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#5536aa",
                            size: "m"
                        });
                    } //For Oct 23, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1023Z0005')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#7a3daa",
                            size: "m"
                        });
                    } //For Oct 26, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1026A0049')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#a4aa12",
                            size: "m"
                        });
                    } //For Oct 26, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1026A0052')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#8aaa14",
                            size: "m"
                        });
                    } //For Oct 27, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1027A0064')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#53aa10",
                            size: "m"
                        });
                    } //For Oct 28, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1028A0055')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#aa660b",
                            size: "m"
                        });
                    } //For Oct 28, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1028A0069')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#aa9123",
                            size: "m"
                        });
                    } //For Oct 28, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1028A0071')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#aa8b57",
                            size: "m"
                        });
                    } //For Oct 28, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1028A0078')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#aa8576",
                            size: "m"
                        });
                    } //For Oct 28, 2018 Photos
                    else if(feature.properties.Name.indexOf('D1028A0079')!==-1){
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#aa4513",
                            size: "m"
                        });
                    }
                    else{
                        surveyedCo_Marker = MakiMarkers.default.icon({
                            id:feature.properties.Name,
                            icon: "camera",
                            color: "#3300ff",
                            size: "m"
                        });
                    }
                    //sortiesMarkerAry.push(surveyedCo_Marker);
                    return L.marker(latlng, {icon: surveyedCo_Marker,autoPan:true})
                },
                onEachFeature: function(feature,layer){
                    //collectSortieQueryMetadata(feature.properties.SortieSearch);
                    let popupContentSorties = "<p><span id='"+feature.properties.Name+"' style='font-weight:bold'>Name: "+feature.properties.Name+"</span>" +
                        //"<br/><a href='+feature.properties.SourceImage+' target='_blank'">"Get Full Size Image</a>" +
                        "<br/><a href='"+feature.properties.SourceImage+"' target='_blank'><img width='300' height='200' src='"+feature.properties.Thumbnail+"'/></a>" +
                        "<br/><span style='font-weight: bold'>Date/Time "+feature.properties.Collect_Date+ " " +feature.properties.Collect_Time +"</span>" +
                        "<br/><span style='font-weight: bold'>Altitude "+feature.properties.GPS_Altitude+ "</span>" +
                        "<br/><span style='font-weight: bold'>Latitude "+ Math.round10(feature.properties.Lat_Node,-6) + "</span>" +
                        "<br/><span style='font-weight: bold'>Longitude "+ Math.round10(feature.properties.Lng_Node,-6) + "</span>" +
                        "<br/><a href='"+feature.properties.SourceImage+"' target='_blank'> Get Full Size Image</a>" +
                        "<br/><br/><span id='PhotoID"+feature.properties.Image_ID+"First' style='font-weight: bold;padding-right:10px;' onkeydown='retrieveNextPhotoKeyboards(\""+feature.properties.Name+"\",\"decrement\",\"event\",+feature.properties.Prev_ID+,\""+feature.properties.Img_Position+"\");' onclick='retrieveNextPhoto(\""+feature.properties.Name+"\",\"decrement\","+feature.properties.Prev_ID+",\""+feature.properties.Last_Img_Position+"\");' class='"+feature.properties.Img_Position+"' >" +
                        "<i style='line-height: 1.3;padding-right:3px;' class=\"fa fa-2x fa-arrow-circle-o-left\" aria-hidden=\"true\"></i>Previous Image</span>" +
                        "<span id='finalIndicatorFirstMsg' style='font-weight: bold;display:none;padding-right:10px'>First Image of Block!</span>"+
                        "<span id='PhotoID"+feature.properties.Image_ID+"' class='"+feature.properties.Img_Position+"' style='font-weight: bold' onkeydown='retrieveNextPhotoKeyboards(\""+feature.properties.Name+"\",\"increment\",+feature.properties.Next_ID+,\""+feature.properties.Img_Position+"\");' onclick='retrieveNextPhoto(\""+feature.properties.Name+"\",\"increment\","+feature.properties.Next_ID+",\""+feature.properties.Next_Img_Position+"\");' class='"+feature.properties.Img_Position+"' >" +
                        "Next Image<i style='line-height: 1.3;padding-left:3px;' class=\"fa fa-2x fa-arrow-circle-o-right\" aria-hidden=\"true\"></i></span>" +
                        "<span id='finalIndicatorMsg' style='font-weight: bold;display:none;padding-right:10px'>No More Images</span>"+
                        "</p>";
                    layer._polygonId = feature.properties.Name;
                    layer.bindPopup(popupContentSorties).on('click',clickZoomedSortie);
                    sortiesMarkerAry.push(layer);

                }
            });

        movesMap.addLayer(geoJsonSorties);
        //[-96.0998,28.8913583333,-95.365165,29.9046483333]
        console.log(incomingData.bbox);
        let sortieQueryBounds = incomingData.bbox;
        let sortieQueryBoundsSplitterAry = sortieQueryBounds.split(",");
        let sortieQueryBoundsAry1 = [parseFloat(sortieQueryBoundsSplitterAry[1]),parseFloat(sortieQueryBoundsSplitterAry[0].replace("[",""))];
        let sortieQueryBoundsAry2 = [parseFloat(sortieQueryBoundsSplitterAry[3].replace("]","")),parseFloat(sortieQueryBoundsSplitterAry[2])];
        let sortieQueryAryAry = [sortieQueryBoundsAry1,sortieQueryBoundsAry2];
        //console.log(sortieQueryAryAry);
        movesMap.fitBounds(geoJsonSorties.getBounds().pad(0.75));
        //$('#sortieMsg').text(collectDateQuery + " Photos");  //Commented bc we arent using JQuery... yet BAP Feb 22, 2019

    }

    //http://129.116.70.166/ida_txcap/api/txCap/envelope/-97.730743/30.926077/-93.619164/34.965345

    function sortieCountEnvelopeFirst(){
        this.clearTxCapPhotoTour();
        this.txCapQuerySpatial = movesMap.getBounds().toBBoxString().replace(/,/g,'/');
        let queryString = 'http://129.116.70.166/ida_txcap/api/txCap/envelope/'+this.txCapQuerySpatial;

        axios.get(queryString)
            .then(response=>{
                //console.log("I am right before the count of records");
                //console.log(response.data.features[0].properties.count_of_records);
                //sortiesLayerFunc(response.data);
                try {
                    let countReturnedRecords = parseInt(response.data.features[0].properties.count_of_records);
                    if (!isNaN(countReturnedRecords) && countReturnedRecords!==0) {
                        this.txCapQueryTotalRecordsCount = countReturnedRecords;
                        //this.txCapQueryCurrentDate = incomingDate;
                        //this.$eventHub.$emit('incomingTxCapCalendarQueryCounts', this.txCapQueryTotalRecordsCount,this.txCapQueryCurrentDate);
                        this.$eventHub.$emit('incomingTxCapSpatialQueryCounts', this.txCapQueryTotalRecordsCount);
                    }
                } catch(exception){
                    console.log(exception.toString())
                }
            })
            .catch(error=>{
                console.log(error);
            });

    }
    function sortieCountEnvelope(incomingStartRecord){
        //this.clearTxCapPhotoTour();
        let recordCountDateQuery = incomingStartRecord*500;
        if(this.txCapQueryTotalRecordsCount < recordCountDateQuery){
            recordCountDateQuery = this.txCapQueryTotalRecordsCount;
        }
        let adjPageNumber = incomingStartRecord-1;
        let startRecord = adjPageNumber*500;

        //this.txCapQuerySpatial = movesMap.getBounds().toBBoxString().replace(/,/g,'/');
        //http://localhost:3000/bldgs_simulator/txCap/-95.730743/29.926077/-95.619164/29.965345
        //http://129.116.70.166/ida_txcap/api/txCap/envelope/offset/-97.730743/30.926077/-93.619164/34.965345/0
        let queryString = 'http://129.116.70.166/ida_txcap/api/txCap/envelope/offset/'+this.txCapQuerySpatial+'/'+startRecord;
        axios.get(queryString)
            .then(response=>{
                //return response.data
                //handleGauges(response.data,incomingMap)
                collectDateQuery = response.data.features[0].properties.Collect_Date;
                console.log(response.data);
                console.log(collectDateQuery);
                sortiesLayerFunc(response.data);
            })
            .catch(error=>{
                console.log(error);
            });

    }


    function sortiesMarkerPopup(incomingId){
        console.log(incomingId + " with the incomingId");
        let justPhotoNum = incomingId.replace("#","");
        if(justPhotoNum.lastIndexOf("First")!==-1){
            justPhotoNum = justPhotoNum.replace("First","");
        }
        for (let i in sortiesMarkerAry){
            let objTest = $(sortiesMarkerAry[i].getPopup()._content);
            //var objTest = $(this.getPopup()._content);
            //console.log($(this.parentNode));
            //console.log(objTest[0].childNodes.item(0).id);
            //console.log(objTest[0].childNodes.item(17).id);
            //let onclickStuff = objTest[0].childNodes.item(17).attributes[3].value;
            //console.log(onclickStuff.lastIndexOf("first"));
            //if(onclickStuff.lastIndexOf('first')!==-1){
            //    console.log(onclickStuff);
            //}
            let markerID = objTest[0].childNodes.item(17).id;
            //console.log(sortiesMarkerAry[3].options.id);
            if (markerID === justPhotoNum){
                if(incomingId.lastIndexOf("First")!==-1) {
                    console.log(objTest[0].childNodes.item(17));
                    let flagger = "#" + objTest[0].childNodes.item(18).id;
                    //console.log(flagger);
                    //$(flagger).toggle();
                    //"font-weight: bold;display:none;padding-right:10px"
                    //objTest[0].childNodes.item(17).style = "font-weight: bold;display:block;padding-right:10px";
                    console.log(objTest[0].childNodes.item(18));
                }
                //console.log("I made it here again");
                //console.log(sortiesMarkerAry[0]);
                sortiesMarkerAry[i].openPopup();
            }
        }
    }


    function FactorySortieQueryMetadata() {
        //var aryPhotos = [];
        //var aryPhotoName = []
        return {
            "sortieName": null,
            "sortieQueryPhotoCount": 0,
            "photoNameArray":[],
            "sortiePhotoArray": []

        };
        //return sortieMetadata;
    }

    /****************
     *
     * @type {Array}
     *
     * The following variables are tied to the clearTxCapPhotoTour Function
     *  and so they are here rather at the top of the .js file
     *
     * **************/

    let arySortiesInQuery = [];
    let firstQuerySortiesFlag = true;
    let counter = 0;
    let sortieQueryMetaCollections;
   //let sortieQueryMC_WeakMap = new WeakMap();
    let sortiesMarkerAry = [];

    function clearTxCapPhotoTour(){
        arySortiesInQuery = [];
        firstQuerySortiesFlag = true;
        counter = 0;
        sortieQueryMetaCollections = null;
        //sortieQueryMC_WeakMap.clear();
        sortiesMarkerAry = [];
        if(movesMap.hasLayer(geoJsonSorties)) {
            console.log("made it here");
            movesMap.removeLayer(geoJsonSorties);
        }
        this.txCapQueryTotalRecordsCount = null;
        this.txCapQueryCurrentDate = null;
        this.txCapQuerySpatial = null;
        this.$eventHub.$emit('resetPagination');
        //resetPagination

    }

    function collectSortieQueryMetadata(incomingSortiePhotoInfo){
        let sortieFactoryId;
        if(firstQuerySortiesFlag){
            arySortiesInQuery = [];
            firstQuerySortiesFlag = false;
            sortieQueryMetaCollections = {};

        }
        if(arySortiesInQuery.indexOf(incomingSortiePhotoInfo.sortieName)===-1) {
            arySortiesInQuery.push(incomingSortiePhotoInfo.sortieName);
            sortieFactoryId = "sortieName" + counter;
            sortieQueryMetaCollections[sortieFactoryId] = FactorySortieQueryMetadata();
            sortieQueryMetaCollections[sortieFactoryId].sortieName = incomingSortiePhotoInfo.sortieName;
            sortieQueryMetaCollections[sortieFactoryId].photoNameArray.push(incomingSortiePhotoInfo.photoName);
            sortieQueryMetaCollections[sortieFactoryId].sortiePhotoArray.push(parseInt(incomingSortiePhotoInfo.photoNumber.replace(/^0+/, '')));
            counter = counter + 1;
            //console.log(sortieQueryMetaCollections[sortieFactoryId]);
        }
        else {

            //reallyIHave2DoThis_4CollectSortieMetadata(incomingSortiePhotoInfo.sortieName);

            let indexForReals = reallyIHave2DoThis_4CollectSortieMetadata(incomingSortiePhotoInfo.sortieName);
            sortieQueryMetaCollections[indexForReals].photoNameArray.push(incomingSortiePhotoInfo.photoName);
            sortieQueryMetaCollections[indexForReals].sortiePhotoArray.push(parseInt(incomingSortiePhotoInfo.photoNumber.replace(/^0+/, '')));
        }


        //console.log(sortieQueryMetaCollections);

    }

    function reallyIHave2DoThis_4CollectSortieMetadata(incomingSortieName) {
        return $.map(sortieQueryMetaCollections, function (obj, index) {
            //console.log(sortieQueryMetaCollections);
            //console.log(index + " ?");
            if (obj.sortieName === incomingSortieName) {
                return index;
            }
        });
    }

    function clickZoomedSortie(e){
        movesMap.panTo(this.getLatLng());
        let objTest = $(this.getPopup()._content);
        //console.log(objTest);
        //  UNCHECK THIS ONE FOR DEBUG console.log($(this.parentNode));
        //console.log(objTest[0].childNodes.item(0));
        let grabDecrementAttributes = objTest[0].childNodes.item(15).attributes[3].value;
        let decrementCurrentPositionAttribute = objTest[0].childNodes.item(15).attributes[4].value;
        //console.log(grabDecrementAttributes);
        let grabIncrementAttributes = objTest[0].childNodes.item(17).attributes[3].value;
        let incrementCurrentPositionAttribute = objTest[0].childNodes.item(17).attributes[4].value;
        //console.log(grabIncrementAttributes);
        //let flagger = "#" + objTest[0].childNodes.item(18).id;
        //console.log(flagger);

        if(grabDecrementAttributes.lastIndexOf('first')!==-1 && decrementCurrentPositionAttribute.lastIndexOf('first')!==-1){
            console.log('do sumpin');
            let firstIdSortie = "#" + objTest[0].childNodes.item(15).id;
            $(firstIdSortie).siblings("#finalIndicatorFirstMsg").toggle();
            $(firstIdSortie).toggle();
        }
        if(grabIncrementAttributes.lastIndexOf('last')!==-1 && incrementCurrentPositionAttribute.lastIndexOf('last')!==-1){
            //console.log('do last sumpin');
            let lastIdSortie = "#" + objTest[0].childNodes.item(17).id;
            $(lastIdSortie).siblings('#finalIndicatorMsg').toggle();
            $(lastIdSortie).toggle();
        }
        //$(flagger).toggle();
        //this._leaflet_id
        //  UNCHECK THIS ONE FOR DEBUG console.log($(this));
        //  UNCHECK THIS ONE FOR DEBUG console.log($(mapFocus));
    }

    function handleSortieLayerEvents(layer){
        onEachSortieFeature(layer.feature,layer);
    }

    function onEachSortieFeature(feature, layer) {
        //console.log(feature.geometry.coordinates[0] + " this is the feature object");
        var popupContent =
            "<p><span style='font-weight:bold'>Name: "+feature.properties.Name+"</span>" +                                                   // + getInundationMax(feature.properties.UTMB_ID) +
            //"<br/><a href='+feature.properties.SourceImage+' target='_blank'">"Get Full Size Image</a>" +
            "<br/><img width='300' height='200' src='"+feature.properties.Thumbnail+"'/>" +
            "<br/><span style='font-weight: bold'>Date/Time "+feature.properties.Collect_Date+ " " +feature.properties.Collect_Time +"</span>" +
            "<br/><span style='font-weight: bold'>Altitude "+feature.properties.GPS_Altitude+ "</span>" +
            "<br/><span style='font-weight: bold'>Latitude "+ Math.round10(feature.properties.lat_node,-6) + "</span>" +
            "<br/><span style='font-weight: bold'>Longitude "+ Math.round10(feature.properties.lng_node,-6) + "</span>" +
            "<br/><a href='"+feature.properties.SourceImage+"' target='_blank'> Get Full Size Image</a>" +
            "</p>";

        if (feature.properties && feature.properties.popupContent) {
            popupContent += feature.properties.popupContent;
        }
        //layer._polygonId = feature.properties.name;
        layer._polygonId = feature.properties.UTMB_ID;
        //console.log(layer._polygonId);

        layer.bindPopup(popupContent,{maxWidth:400});

        //mapFocus.panTo([latMarker, longMarker]);

    }
</script>

<style scoped>
    #mapTexas{
        width: 100%;
        height: inherit;
    }

</style>