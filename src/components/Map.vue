<template>
    <div id="mapTexas"></div>
</template>

<script>
    import L from "leaflet";
    import * as esri from "esri-leaflet";
    import * as wmts from 'leaflet-tilelayer-wmts';
    import axios from 'axios';
    import * as MakiMarkers from './scripts/Leaflet.MakiMarkers';
    import './scripts/utility';

    let movesMap;
    let esriAerialsLayer;
    let esriAerialsLabels;
    let esriToposLayer;
    let esriStreetsLayer;
    let googleImageryLayer;
    let geoJsonQPF_Day1;
    let geoJsonQPF_Day2;
    let maskingSentinelApr16;


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
            addRemoveMaskTornado:addRemoveMaskTornado,
            resetMap,
            redrawMap,
            goToBookmark,
            goToLocation,
            getMapInfo
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
                ]
            });
/*            geoJsonQPF_Day1 = L.geoJson(qpfDay1,
                {
                    style: function(feature) {
                        switch (feature.properties.QPF) {
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

                });*/

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
        },
        created(){
            //Menu Components used to pass over Global Event hub these events from buttons
            this.$eventHub.$on('toggleMapLayers', this.toggleLayer);
            this.$eventHub.$on('resetMap',this.resetMap);
            this.$eventHub.$on('goToBookmarks',this.goToBookmark);
            this.$eventHub.$on('goToLocation',this.goToLocation);
            //this.$eventHub.$on('goToLocation',this.goToNamedLocation);
            this.$eventHub.$on('gatheringMapInfo',this.getMapInfo);
            this.$eventHub.$on('redrawMap',this.redrawMap);
            //toggleMaskTornado20190416
            this.$eventHub.$on('toggleMaskTornado20190416', this.addRemoveMaskTornado);
        }
    }


    function resetMap(){
        movesMap.setView([32.3117, -99.77774], 6);
        movesMap.invalidateSize();
    }

    function redrawMap(){
        console.log('Here');
        movesMap.invalidateSize();
    }

    function getMapInfo(){
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





</script>

<style scoped>
    #mapTexas{
        width: 100%;
        height: inherit;
    }

</style>
